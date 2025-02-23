import time
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
import logging

# Setup logging
logging.basicConfig(filename="performance.log", level=logging.INFO, format="%(asctime)s - %(message)s")

class PerformanceMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = (time.time() - start_time)
        logging.info(f"{request.method} {request.url} - {process_time:.2f} ms")
        response.headers["API-Process-Time"] = str(process_time)  # Add response to headers
        return response
