from sqlalchemy import Column, Integer, ForeignKey
from app.database.db import Base

class Booking(Base):
    __tablename__ = "bookings"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True) # Later we link to User.id
    event_id = Column(Integer, ForeignKey("events.id"))