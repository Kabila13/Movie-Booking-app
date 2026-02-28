from pydantic import BaseModel

class EventCreate(BaseModel):
    title: str
    description: str
    total_seats: int

class EventResponse(BaseModel):
    id: int
    title: str
    description: str
    total_seats: int
    available_seats: int

    class Config:
        from_attributes = True