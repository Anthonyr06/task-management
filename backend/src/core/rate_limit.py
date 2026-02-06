import time
from fastapi import HTTPException
from src.core.redis import get_redis

def rate_limit(key: str, limit: int, window_seconds: int):
    r = get_redis()
    now = int(time.time())
    bucket = now // window_seconds
    redis_key = f"rl:{key}:{bucket}"

    count = r.incr(redis_key)
    if count == 1:
        r.expire(redis_key, window_seconds)

    if count > limit:
        raise HTTPException(status_code=429, detail="Too many requests")
