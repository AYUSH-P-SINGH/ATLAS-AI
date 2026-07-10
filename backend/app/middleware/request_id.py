import uuid
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware


class RequestIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Extract existing Request ID or generate a new UUID
        request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
        
        # Attach request ID to request state so other middlewares or controllers can access it
        request.state.request_id = request_id
        
        # Process the request
        response: Response = await call_next(request)
        
        # Return the Request ID back in response headers for client tracing
        response.headers["X-Request-ID"] = request_id
        return response
