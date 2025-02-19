from fastapi import FastAPI, Header, HTTPException, Depends
from pydantic import BaseModel
import os
from fastapi.middleware.cors import CORSMiddleware
import random

app = FastAPI()

# CORS setup
origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in origins],
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["X-API-Key", "Content-Type"],
)

# Mock API key auth
API_KEYS = os.getenv("API_KEYS", "test-key").split(",")

async def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key not in API_KEYS:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return x_api_key

class InferenceInput(BaseModel):
    title: str
    company: str
    location: str
    description: str
    skills: str
    experience_from: int
    experience_to: int

@app.get("/healthcheck")
async def healthcheck():
    return {"status": "ok"}

@app.post("/predict", dependencies=[Depends(verify_api_key)])
async def predict(input_data: InferenceInput):
    # Mock prediction - returns random salary between 40000-80000
    mock_salary = random.uniform(40000, 80000)
    return {"predicted_salary": mock_salary}
