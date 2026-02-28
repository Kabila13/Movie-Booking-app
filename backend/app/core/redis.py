import redis
import time

# Connect to Redis [cite: 8, 9]
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

def acquire_lock(event_id, timeout=10):
    lock_key = f"lock:event:{event_id}"
    while timeout > 0:
        # SETNX (Set if Not Exists) acts as a lock 
        if redis_client.setnx(lock_key, "locked"):
            redis_client.expire(lock_key, 10) # Auto-release after 10s
            return True
        time.sleep(0.1)
        timeout -= 0.1
    return False

def release_lock(event_id):
    redis_client.delete(f"lock:event:{event_id}")