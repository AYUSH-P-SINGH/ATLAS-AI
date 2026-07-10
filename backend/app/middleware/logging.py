import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from loguru import logger


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Resolve trace ID from request state
        request_id = getattr(request.state, "request_id", "unknown")
        method = request.method
        path = request.url.path
        
        logger.info(
            f"Incoming Request - Method: {method} | Path: {path} | RequestID: {request_id}"
        )
        
        start_time = time.time()
        try:
            response = await call_next(request)
            process_time = (time.time() - start_time) * 1000  # ms
            
            logger.info(
                f"Outgoing Response - Method: {method} | Path: {path} | Status: {response.status_code} | "
                f"Duration: {process_time:.2f}ms | RequestID: {request_id}"
            )
            return response
        except Exception as e:
            process_time = (time.time() - start_time) * 1000
            # log stacktrace with logger.exception
            logger.exception(
                f"Request Exception - Method: {method} | Path: {path} | Error: {str(e)} | "
                f"Duration: {process_time:.2f}ms | RequestID: {request_id}"
            )
            raise e
