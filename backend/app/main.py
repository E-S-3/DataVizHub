from fastapi import FastAPI
from app.api.router import router
from app.middleware import PerformanceMiddleware

app = FastAPI()
app.include_router(router)
app.add_middleware(PerformanceMiddleware)