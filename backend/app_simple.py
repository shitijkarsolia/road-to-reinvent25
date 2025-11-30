"""
Lucky Loo - Simplified Backend (No Strands - Mock Only)
Troubleshooting version
"""

import os
from typing import Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

from mock_responses import get_mock_response

# Models
class PleaRequest(BaseModel):
    plea: str
    image_base64: Optional[str] = None
    demo_mode: bool = False

class JuryVotes(BaseModel):
    skeptic: str
    doctor: str
    gambler: str

class VerdictResponse(BaseModel):
    verdict: str
    reasoning: str
    roast: str
    jury_votes: JuryVotes

# App
app = FastAPI(title="Lucky Loo API (Simple)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"status": "running", "message": "Lucky Loo Simple API"}

@app.get("/api/health")
async def health():
    return {"status": "healthy"}

@app.post("/api/judge", response_model=VerdictResponse)
async def submit_plea(request: PleaRequest):
    """Mock-only version for testing"""
    if request.demo_mode:
        result = {
            "verdict": "GRANTED",
            "reasoning": "DEMO MODE",
            "roast": "VIP access!",
            "jury_votes": {"skeptic": "REAL", "doctor": "CRITICAL", "gambler": "IN"}
        }
    else:
        result = get_mock_response()
    
    return VerdictResponse(**result)

@app.post("/api/demo", response_model=VerdictResponse)
async def demo():
    result = {
        "verdict": "GRANTED",
        "reasoning": "DEMO MODE",
        "roast": "VIP access!",
        "jury_votes": {"skeptic": "REAL", "doctor": "CRITICAL", "gambler": "IN"}
    }
    return VerdictResponse(**result)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app_simple:app", host="0.0.0.0", port=8000, reload=True)

