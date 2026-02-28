from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.schemas.event import EventCreate
from app.database import models
# CRITICAL: Import your JWT handler here
from app.core.jwt_handler import get_current_user 

router = APIRouter(prefix="/events", tags=["Events"])

# --- Helper Dependency ---
def admin_only(current_user = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Access denied. Admins only."
        )
    return current_user

# --- Routes ---

@router.get("/")
def get_all_events(db: Session = Depends(get_db)):
    return db.query(models.Event).all()

@router.post("/")
def create_event(event: EventCreate, db: Session = Depends(get_db), _ = Depends(admin_only)):
    new_event = models.Event(
        title=event.title,
        description=event.description,
        total_seats=event.total_seats,
        available_seats=event.total_seats
    )
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    return new_event

@router.delete("/{event_id}")
def delete_event(event_id: int, db: Session = Depends(get_db), _ = Depends(admin_only)):
    event = db.query(models.Event).filter(models.Event.id == event_id).first()
    
    if not event:
        raise HTTPException(status_code=404, detail=f"Event ID {event_id} not found")
    
    # Optional: Delete bookings for this event first
    db.query(models.Booking).filter(models.Booking.event_id == event_id).delete()
    
    db.delete(event)
    db.commit()
    return {"message": "Event deleted successfully"}