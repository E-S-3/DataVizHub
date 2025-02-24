from fastapi import FastAPI, HTTPException, Depends
from app.api.router import router
from app.middleware import PerformanceMiddleware
from fastapi.middleware.cors import CORSMiddleware
from app.firebase_config import auth
from pydantic import BaseModel


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

# Model for receiving Google ID token
class TokenRequest(BaseModel):
    token: str

@app.post("/login")
async def google_auth(token_data: TokenRequest):
    try:
        # Verify Firebase token
        user = auth.sign_in_with_custom_token(token_data.token)
        user_id = user["localId"]
        return {"message": "User authenticated", "uid": user_id}
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.get("/logout")
async def logout():
    return {"message": "Logged out successfully"}