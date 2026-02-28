from app.database.db import SessionLocal
from app.database import models

def reset_database():
    db = SessionLocal()
    try:
        print("Cleaning up old data...")
        # 1. Delete Bookings first (because they depend on Events)
        db.query(models.Booking).delete()
        # 2. Delete all existing Events
        db.query(models.Event).delete()
        
        print("Creating fresh movies...")
        # 3. Create New Events
        new_movies = [
            models.Event(
                title="Avatar: The Way of Water", 
                description="Jake Sully lives with his newfound family formed on the extrasolar moon Pandora.", 
                available_seats=150, 
                total_seats=150
            ),
            models.Event(
                title="Oppenheimer", 
                description="The story of American scientist, J. Robert Oppenheimer, and his role in the development of the atomic bomb.", 
                available_seats=80, 
                total_seats=80
            ),
            models.Event(
                title="Spider-Man: Across the Spider-Verse", 
                description="Miles Morales catapults across the Multiverse.", 
                available_seats=120, 
                total_seats=120
            )
        ]
        
        db.add_all(new_movies)
        db.commit()
        print("✅ Success! Database is fresh and ready for the demo.")
        
    except Exception as e:
        print(f"❌ Error during seeding: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    reset_database()