from sqlalchemy import func
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.db import SessionLocal
from app.database import models

router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/event/{event_id}")
def event_report(event_id: int, db: Session = Depends(get_db)):

    event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    total_bookings = db.query(models.Booking).filter(
        models.Booking.event_id == event_id
    ).count()

    return {
        "event_id": event.id,
        "event_name": event.title,
        "total_bookings": total_bookings,
        "available_seats": event.available_seats
    }
@router.get("/total")
def get_total_bookings(db: Session = Depends(get_db)):
    """Returns the total number of bookings across the entire platform"""
    count = db.query(models.Booking).count()
    return {"total_system_bookings": count}

@router.get("/all-events-summary")
def get_all_events_report(db: Session = Depends(get_db)):
    """Returns a list of all events with their current booking counts"""
    # This query joins Event and Booking to count bookings per event
    results = db.query(
        models.Event.title,
        func.count(models.Booking.id).label("total")
    ).outerjoin(models.Booking).group_by(models.Event.id).all()
    
    return [{"event_name": r[0], "bookings": r[1]} for r in results]

@router.get("/user-history/{user_id}")
def get_user_history(user_id: int, db: Session = Depends(get_db)):
    """Returns all bookings made by a specific user"""
    history = db.query(models.Booking).filter(models.Booking.user_id == user_id).all()
    return {
        "user_id": user_id,
        "history": history
    }