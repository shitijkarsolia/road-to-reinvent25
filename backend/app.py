"""
Lucky Loo - FastAPI Backend
The High-Stakes Restroom Finder API

Endpoints:
- POST /api/judge - Submit a plea for bathroom access
- GET /api/health - Health check
- POST /api/demo - Demo mode (always wins)
"""

import os
import json
import base64
from typing import Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import our agents
from agents import run_court_of_relief


# ============================================================================
# PYDANTIC MODELS
# ============================================================================

class PleaRequest(BaseModel):
    """Request body for bathroom access plea."""
    plea: str
    image_base64: Optional[str] = None
    demo_mode: bool = False


class JuryVotes(BaseModel):
    """Individual jury member votes."""
    skeptic: str
    doctor: str
    gambler: str


class VerdictResponse(BaseModel):
    """Response from the Court of Relief."""
    verdict: str  # "GRANTED" or "DENIED"
    reasoning: str
    roast: str
    jury_votes: JuryVotes


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    service: str
    version: str


# ============================================================================
# APP SETUP
# ============================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    print("🚽 Lucky Loo Court of Relief is now in session!")
    yield
    print("🎰 Court adjourned. House always wins.")


app = FastAPI(
    title="Lucky Loo API",
    description="The High-Stakes Restroom Finder - Prove your desperation to the AI Jury",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# ENDPOINTS
# ============================================================================

@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        service="lucky-loo-court",
        version="1.0.0"
    )


@app.post("/api/judge", response_model=VerdictResponse)
async def submit_plea(request: PleaRequest):
    """
    Submit a plea for bathroom access to the Court of Relief.
    
    The AI Jury (The Skeptic, The Doctor, The Gambler) will deliberate,
    and The Pit Boss will deliver the final verdict.
    """
    try:
        # Validate plea
        if not request.plea or len(request.plea.strip()) < 3:
            raise HTTPException(
                status_code=400,
                detail="Your plea must be at least 3 characters. The Court requires substance."
            )
        
        # Run the Court of Relief
        result = run_court_of_relief(
            user_plea=request.plea,
            image_base64=request.image_base64,
            demo_mode=request.demo_mode
        )
        
        return VerdictResponse(
            verdict=result.get("verdict", "DENIED"),
            reasoning=result.get("reasoning", "The Court has ruled."),
            roast=result.get("roast", "No comment."),
            jury_votes=JuryVotes(**result.get("jury_votes", {
                "skeptic": "UNKNOWN",
                "doctor": "UNKNOWN",
                "gambler": "UNKNOWN"
            }))
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Court error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"The Court experienced an unexpected error: {str(e)}"
        )


@app.post("/api/judge/upload")
async def submit_plea_with_image(
    plea: str = Form(...),
    demo_mode: bool = Form(False),
    image: Optional[UploadFile] = File(None)
):
    """
    Submit a plea with an uploaded image file.
    Alternative to base64 encoding for easier frontend integration.
    """
    try:
        image_base64 = None
        
        if image:
            # Read and encode the image
            contents = await image.read()
            image_base64 = base64.b64encode(contents).decode('utf-8')
        
        # Run the Court of Relief
        result = run_court_of_relief(
            user_plea=plea,
            image_base64=image_base64,
            demo_mode=demo_mode
        )
        
        return VerdictResponse(
            verdict=result.get("verdict", "DENIED"),
            reasoning=result.get("reasoning", "The Court has ruled."),
            roast=result.get("roast", "No comment."),
            jury_votes=JuryVotes(**result.get("jury_votes", {
                "skeptic": "UNKNOWN",
                "doctor": "UNKNOWN",
                "gambler": "UNKNOWN"
            }))
        )
        
    except Exception as e:
        print(f"Court error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"The Court experienced an unexpected error: {str(e)}"
        )


@app.post("/api/demo", response_model=VerdictResponse)
async def demo_mode():
    """
    Demo mode endpoint - always grants access.
    Use this for stage presentations.
    """
    result = run_court_of_relief(
        user_plea="Demo mode activated",
        demo_mode=True
    )
    
    return VerdictResponse(
        verdict=result.get("verdict", "GRANTED"),
        reasoning=result.get("reasoning", "DEMO MODE ACTIVE"),
        roast=result.get("roast", "VIP access granted."),
        jury_votes=JuryVotes(**result.get("jury_votes", {
            "skeptic": "REAL",
            "doctor": "CRITICAL",
            "gambler": "IN"
        }))
    )


@app.get("/")
async def root():
    """Root endpoint with API info."""
    return {
        "name": "Lucky Loo - Court of Relief API",
        "tagline": "Because in Vegas, even a flush is a gamble.",
        "endpoints": {
            "health": "GET /api/health",
            "judge": "POST /api/judge",
            "judge_upload": "POST /api/judge/upload",
            "demo": "POST /api/demo"
        },
        "jury": ["The Skeptic", "The Doctor", "The Gambler"],
        "judge": "The Pit Boss"
    }


# ============================================================================
# RUN SERVER
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("PORT", 8000))
    
    print(f"""
    🎰 ══════════════════════════════════════════ 🎰
    
       LUCKY LOO - COURT OF RELIEF
       "The High-Stakes Restroom Finder"
       
       Server starting on port {port}...
       
    🎰 ══════════════════════════════════════════ 🎰
    """)
    
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=port,
        reload=True
    )
