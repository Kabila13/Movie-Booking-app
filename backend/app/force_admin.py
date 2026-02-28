from app.database import models
from app.database.db import SessionLocal
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
db = SessionLocal()

email = "admin@test.com"
password = "adminpassword123" # Set your password here

# 1. Check if user exists, if not, create them
user = db.query(models.User).filter(models.User.email == email).first()

if not user:
    print(f"Creating new user: {email}")
    user = models.User(
        email=email,
        password=pwd_context.hash(password),
        name="AdminUser",
        is_admin=True
    )
    db.add(user)
else:
    print(f"Updating existing user: {email}")
    user.is_admin = True
    user.password = pwd_context.hash(password)

db.commit()
print(f"SUCCESS: {email} is now an ADMIN with password: {password}")
db.close()