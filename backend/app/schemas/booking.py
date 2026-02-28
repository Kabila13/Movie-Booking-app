from app.database import redis
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.models.event import Event
from app.models.booking import Booking # Make sure you have a Booking model
from app.schemas.booking import BookingCreate

router = APIRouter(prefix="/bookings", tags=["Bookings"])

# Connect to Redis (Adjust host if using Docker later)
r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

@router.post("/")
def book_ticket(booking_data: BookingCreate, db: Session = Depends(get_db)):
    event_id = booking_data.event_id
    lock_key = f"lock:event:{event_id}"

    # 1. Try to acquire a lock in Redis for 5 seconds
    # This prevents "Race Conditions" (two people buying the same last seat)
    if r.set(lock_key, "locked", nx=True, px=5000):
        try:
            # 2. Check if event exists and has seats
            event = db.query(Event).filter(Event.id == event_id).first()
            if not event:
                raise HTTPException(status_code=404, detail="Event not found")

            if event.available_seats <= 0:
                raise HTTPException(status_code=400, detail="Sold out!")

            # 3. Reduce seat count and save booking
            event.available_seats -= 1
            new_booking = Booking(event_id=event_id, user_id=1) # Hardcoded user_id for now
            
            db.add(new_booking)
            db.commit()
            db.refresh(new_booking)
            
            return {"message": "Booking successful!", "booking_id": new_booking.id}

        finally:
            # 4. Always release the lock so others can buy
            r.delete(lock_key)
    else:
        raise HTTPException(status_code=429, detail="Server busy, please try again.")