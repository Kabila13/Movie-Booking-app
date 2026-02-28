from celery import Celery

# Celery instance
celery_app = Celery(
    "worker",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

@celery_app.task(name="send_booking_confirmation")
def send_booking_confirmation(email, event_title):
    # Simulated email for the project requirement
    print(f"--- MANDATORY NOTIFICATION ---")
    print(f"To: {email}")
    print(f"Message: Ticket confirmed for {event_title}")
    return True