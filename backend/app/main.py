from fastapi import FastAPI
from app.api.router import router
from app.middleware import PerformanceMiddleware
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.include_router(router)
app.add_middleware(PerformanceMiddleware)

from fastapi import FastAPI
from app.api.router import router

# Define allowed origins
origins = [
    "http://localhost:3000",  # Allow requests from React frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow specific origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)