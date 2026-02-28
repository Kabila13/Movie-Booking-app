from fastapi import FastAPI
from app.database.db import engine, Base
from app.database import models
from app.routes import auth, events
from app.routes import bookings
from app.routes import reports
from app.routes import auth, events, bookings
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers (like Authorization)
)


app.include_router(auth.router)
app.include_router(events.router)
app.include_router(bookings.router)
app.include_router(reports.router)

@app.get("/")
def root():
    return {"message": "Ticket Booking API is running"}
