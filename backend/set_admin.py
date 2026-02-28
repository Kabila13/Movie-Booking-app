from app.database import models
from app.database.db import SessionLocal

# Connect to the database
db = SessionLocal()

# Target email
target_email = "admin@test.com" 

# Find the user
user = db.query(models.User).filter(models.User.email == target_email).first()

if user:
    user.is_admin = True
    db.commit()
    print(f"--- SUCCESS ---")
    print(f"User {target_email} is now an ADMIN.")
else:
    print(f"--- ERROR ---")
    print(f"User with email '{target_email}' not found in the database.")

db.close()