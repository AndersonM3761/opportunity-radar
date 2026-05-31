from fastapi import Depends, HTTPException
import fakeredis.aioredis as redis
from app.models.schemas import SearchRequest

# Global instance so memory persists across requests
redis_client = redis.FakeRedis(decode_responses=True)

async def get_redis():
    return redis_client

async def check_rate_limit(request: SearchRequest, redis_db = Depends(get_redis)):
    try:
        # Use email for rate limiting
        key = f"rate_limit:{request.email}"
        exists = await redis_db.get(key)
        if exists:
            raise HTTPException(
                status_code=429,
                detail={"error": "Rate limited. Only one search per 10 minutes allowed.", "retry_after": 600}
            )
        # Block for 10 minutes (600 seconds)
        await redis_db.setex(key, 600, "1")
    except HTTPException:
        # Re-raise the 429 so the user is actually blocked
        raise
    except Exception as e:
        # Fail Open: if Redis is down or unreachable, allow the request through.
        print(f"Redis rate limiter bypassed due to error: {e}")
        pass
