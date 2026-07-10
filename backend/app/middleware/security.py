from fastapi import Request, Response, status
from starlette.middleware.base import BaseHTTPMiddleware
from loguru import logger
import time

# Very basic in-memory rate limiter placeholder
# Tracks IP hits per minute
_rate_limit_db: dict[str, int] = {}


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response: Response = await call_next(request)
        # Prevent Clickjacking
        response.headers["X-Frame-Options"] = "DENY"
        # Prevent MIME type sniffing
        response.headers["X-Content-Type-Options"] = "nosniff"
        # XSS Protection for legacy browsers
        response.headers["X-XSS-Protection"] = "1; mode=block"
        # Control Referrer information sent
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        # Basic Content Security Policy (allows style/scripts of landing page)
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data:; "
            "connect-src 'self' ws: wss:;"
        )
        return response


class RateLimitingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host if request.client else "unknown"
        current_time = int(time.time())
        window = current_time // 60  # 1-minute window
        
        db_key = f"{client_ip}:{window}"
        request_count = _rate_limit_db.get(db_key, 0)
        
        # Rate limit threshold (e.g., 200 requests per minute for local dev)
        threshold = 200
        if request_count >= threshold:
            logger.warning(f"Rate limit exceeded for client: {client_ip}")
            return Response(
                content="Too many requests. Please try again later.",
                status_code=status.HTTP_429_TOO_MANY_REQUESTS
            )
            
        _rate_limit_db[db_key] = request_count + 1
        
        # Cleanup old entries periodically (very basic)
        if len(_rate_limit_db) > 10000:
            _rate_limit_db.clear()
            
        return await call_next(request)
