from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.db import SessionLocal
from app.database import models
from app.core.redis import redis_client
# IMPORT YOUR CELERY TASK
from app.worker.tasks import send_booking_confirmation 
from app.core.jwt_handler import get_current_user

router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# In backend/app/routes/bookings.py

@router.post("/book/{event_id}") # Changed to match dashboard.jsx
def create_booking(
    event_id: int, 
    db: Session = Depends(get_db), 
    current_user = Depends(get_current_user) # Get user from token instead of manual ID
):
    user_id = current_user.id
    seats = 1 # Default to 1 seat for the dashboard button
    lock_key = f"event_lock:{event_id}"

    # 1. Redis locking
    lock = redis_client.set(lock_key, "locked", nx=True, ex=10)
    if not lock:
        raise HTTPException(status_code=400, detail="Another booking is in progress. Try again.")

    try:
        user = db.query(models.User).filter(models.User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        event = db.query(models.Event).filter(models.Event.id == event_id).first()
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")

        if event.available_seats < seats:
            raise HTTPException(status_code=400, detail="Not enough seats available")

        # 2. Update PostgreSQL 
        event.available_seats -= seats
        booking = models.Booking(
            user_id=user_id,
            event_id=event_id,
            seat_number=seats
        )
        db.add(booking)
        db.commit()
        db.refresh(event)

        # 3. Trigger Celery background task for mandatory notifications 
        # This sends the ticket to both User and Admin as required 
        send_booking_confirmation.delay(user.email, event.title)

        return {
            "message": "Booking successful. Confirmation email is being sent.",
            "booking_id": booking.id,
            "remaining_seats": event.available_seats
        }

    finally:
        # Always release Redis lock
        redis_client.delete(lock_key)

@router.get("/user/{user_id}")
def get_user_bookings(user_id: int, db: Session = Depends(get_db)):
    # Satisfies 'User booking history' requirement 
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    bookings = db.query(models.Booking).filter(
        models.Booking.user_id == user_id
    ).all()

    return {
        "user_id": user_id,
        "total_bookings": len(bookings),
        "bookings": bookings
    }

# NEW: Basic reports / summaries requirement 
@router.get("/reports/summary")
def get_booking_summary(db: Session = Depends(get_db)):
    total_bookings = db.query(models.Booking).count()
    return {
        "total_bookings": total_bookings,
        "description": "Summary of all system bookings"
    }

@router.delete("/{booking_id}")
def cancel_booking(booking_id: int, db: Session = Depends(get_db)):
    booking = db.query(models.Booking).filter(
        models.Booking.id == booking_id
    ).first()

    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    event = db.query(models.Event).filter(
        models.Event.id == booking.event_id
    ).first()

    event.available_seats += booking.seat_number
    db.delete(booking)
    db.commit()
    db.refresh(event)

    return {
        "message": "Booking cancelled successfully",
        "restored_seats": booking.seat_number,
        "available_seats": event.available_seats
    }

@router.get("/my-bookings")
def get_my_bookings(
    db: Session = Depends(get_db), 
    current_user = Depends(get_current_user)
):
    # This automatically finds the ID of the person logged in
    bookings = db.query(models.Booking).filter(
        models.Booking.user_id == current_user.id
    ).all()
    
    return bookings