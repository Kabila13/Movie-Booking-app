from sqlalchemy import Column, Integer, String
from app.database.db import Base

class Event(Base):
    __tablename__ = "events"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    total_seats = Column(Integer, nullable=False)
    available_seats = Column(Integer, nullable=False)
