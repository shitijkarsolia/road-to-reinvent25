"""
Lucky Loo - The Court of Relief
AI Jury & Judge system using AWS Strands Agents with Bedrock Vision

This module implements the "Agents-as-Tools" pattern where:
- The Jury (Skeptic, Doctor, Gambler) are child agents
- The Judge (Pit Boss) orchestrates them and delivers the final verdict
"""

import os
import json
import random
import base64
import boto3
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from strands import Agent, tool
from strands.models import BedrockModel

# Import mock responses for offline testing
from mock_responses import get_mock_response

# Check if we're in mock mode (no AWS credentials)
MOCK_MODE = os.getenv("MOCK_MODE", "false").lower() == "true"

# Load steering prompts from markdown files
STEERING_DIR = Path(__file__).parent / "steering"


def load_steering_prompt(filename: str) -> str:
    """Load a steering prompt from the steering directory."""
    filepath = STEERING_DIR / filename
    if filepath.exists():
        return filepath.read_text()
    return ""


# Initialize Bedrock model - Claude Sonnet 4.5 with vision
MODEL_ID = os.getenv("BEDROCK_MODEL_ID", "us.anthropic.claude-sonnet-4-5-20250929-v1:0")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

print(f"🎰 Using model: {MODEL_ID}")
print(f"🌎 Region: {AWS_REGION}")

bedrock_model = BedrockModel(
    model_id=MODEL_ID,
    region_name=AWS_REGION
)

# Bedrock runtime client for direct vision calls
bedrock_runtime = boto3.client(
    service_name="bedrock-runtime",
    region_name=AWS_REGION
)


# ============================================================================
# VISION ANALYSIS - Analyze face with Claude Vision
# ============================================================================

def analyze_face_with_vision(image_base64: str) -> dict:
    """
    Analyze a face image using Claude's vision capabilities.
    Returns analysis of desperation level.
    """
    try:
        message = {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/jpeg",
                        "data": image_base64
                    }
                },
                {
                    "type": "text",
                    "text": """You are a cynical Vegas bouncer analyzing this person's face for signs of BATHROOM DESPERATION.

Look for GENUINE desperation signs:
- Wide, panicked eyes
- Clenched jaw, grimacing
- Sweat on forehead
- Pained or distressed expression
- Tense facial muscles

Look for FAKE desperation signs:
- Relaxed expression trying to look distressed
- Smiling or laughing
- Calm, relaxed features
- Obviously "acting"

Respond in this exact format:
VERDICT: [REAL/FAKE]
CONFIDENCE: [HIGH/MEDIUM/LOW]
ANALYSIS: [One cynical sentence about what you see, in noir detective style]"""
                }
            ]
        }
        
        response = bedrock_runtime.invoke_model(
            modelId=MODEL_ID,
            body=json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 300,
                "messages": [message]
            })
        )
        
        result = json.loads(response["body"].read())
        content = result.get("content", [{}])[0].get("text", "")
        
        # Parse the response
        is_real = "VERDICT: REAL" in content.upper()
        
        return {
            "verdict": "REAL" if is_real else "FAKE",
            "analysis": content
        }
        
    except Exception as e:
        print(f"Vision analysis error: {e}")
        return {
            "verdict": "FAKE",
            "analysis": f"Couldn't see your face clearly. Assuming you're faking it. Error: {str(e)}"
        }


# ============================================================================
# JURY AGENTS
# ============================================================================

juror_skeptic = Agent(
    name="The_Skeptic",
    model=bedrock_model,
    system_prompt=load_steering_prompt("juror_skeptic.md"),
)

juror_doctor = Agent(
    name="The_Doctor", 
    model=bedrock_model,
    system_prompt=load_steering_prompt("juror_doctor.md"),
)

juror_gambler = Agent(
    name="The_Gambler",
    model=bedrock_model,
    system_prompt=load_steering_prompt("juror_gambler.md"),
)


# ============================================================================
# JURY TOOLS
# ============================================================================

@tool
def consult_skeptic(face_analysis: str) -> str:
    """
    Consult The Skeptic with the face analysis results.
    The Skeptic is a cynical Vegas bouncer who detects fake desperation.
    
    Args:
        face_analysis: The vision analysis of the user's face, or note about missing image.
    
    Returns:
        The Skeptic's verdict on whether the desperation is REAL or FAKE.
    """
    prompt = f"""Here is the face analysis from our security cameras:

{face_analysis}

Based on this evidence, deliver your verdict. Are they REAL desperate or FAKE desperate?"""
    
    response = juror_skeptic(prompt)
    return str(response)


@tool  
def consult_doctor(user_plea: str) -> str:
    """
    Consult The Doctor to evaluate the user's plea for medical urgency.
    The Doctor is an overly dramatic medical professional.
    
    Args:
        user_plea: The text the user submitted describing their bathroom need.
    
    Returns:
        The Doctor's dramatic medical diagnosis and urgency assessment.
    """
    prompt = f"""A patient has submitted the following plea for bathroom access:

"{user_plea}"

Provide your medical diagnosis and urgency assessment. Be dramatic."""
    
    response = juror_doctor(prompt)
    return str(response)


@tool
def consult_gambler() -> str:
    """
    Consult The Gambler for a luck-based decision.
    The Gambler doesn't care about facts - only fate and fortune.
    
    Returns:
        The Gambler's chaotic, luck-based verdict.
    """
    luck_seed = random.choice([
        "The dice are hot tonight.",
        "I just saw a black cat. Bad omen.",
        "Someone just hit the jackpot on floor 3. Good vibes.",
        "Mercury is in retrograde. Tread carefully.",
        "I found a penny heads-up this morning. Lucky day.",
        "The cards have been cold all night.",
    ])
    
    prompt = f"""It's time to make your call. {luck_seed}

Should this person get bathroom access? Consult your gambling instincts and deliver your verdict."""
    
    response = juror_gambler(prompt)
    return str(response)


# ============================================================================
# THE JUDGE (PIT BOSS) - Orchestrates the Jury
# ============================================================================

pit_boss_judge = Agent(
    name="Pit_Boss",
    model=bedrock_model,
    tools=[consult_skeptic, consult_doctor, consult_gambler],
    system_prompt=load_steering_prompt("judge_pitboss.md"),
)


# ============================================================================
# MAIN API FUNCTION
# ============================================================================

def run_court_of_relief(
    user_plea: str,
    image_base64: Optional[str] = None,
    demo_mode: bool = False,
    mock_mode: bool = None
) -> dict:
    """
    Run the full Court of Relief deliberation.
    
    Args:
        user_plea: The user's text plea for bathroom access
        image_base64: Optional base64-encoded image of the user's face
        demo_mode: If True, always grants access (for stage demos)
        mock_mode: If True, use mock responses (no AWS calls). Defaults to env var.
    
    Returns:
        dict with verdict, reasoning, roast, and jury_votes
    """
    
    # Check mock mode
    use_mock = mock_mode if mock_mode is not None else MOCK_MODE
    
    # Demo mode - always win for stage presentations
    if demo_mode:
        return {
            "verdict": "GRANTED",
            "reasoning": "DEMO MODE: The Court has been rigged in your favor.",
            "roast": "Jackpot! The Porcelain Gods recognize a VIP when they see one.",
            "jury_votes": {
                "skeptic": "REAL",
                "doctor": "CRITICAL",
                "gambler": "IN"
            }
        }
    
    # Mock mode - use pre-written responses (for testing without AWS)
    if use_mock:
        print("🎭 Running in MOCK MODE - using pre-written responses")
        return get_mock_response()
    
    # Analyze face if image provided
    face_analysis = None
    if image_base64:
        print("👁️ Analyzing face with Claude Vision...")
        vision_result = analyze_face_with_vision(image_base64)
        face_analysis = vision_result.get("analysis", "No analysis available")
        print(f"👁️ Vision result: {vision_result.get('verdict')}")
    
    # Build the case presentation for the Judge
    case_presentation = f"""
A desperate soul seeks bathroom access at Lucky Loo Casino.

USER'S PLEA: "{user_plea}"
"""
    
    if face_analysis:
        case_presentation += f"""
FACE ANALYSIS FROM SECURITY CAMERAS:
{face_analysis}

When consulting The Skeptic, provide this face analysis.
"""
    else:
        case_presentation += """
VISUAL EVIDENCE: None provided. No photo submitted.
When consulting The Skeptic, note that no visual proof was provided.
"""
    
    case_presentation += """
Your task:
1. Call consult_skeptic with the face analysis (or note about missing photo)
2. Call consult_doctor with the user's plea text
3. Call consult_gambler for the luck factor
4. Weigh their opinions and deliver your FINAL VERDICT as JSON

Remember: Your output MUST end with valid JSON in this format:
{
    "verdict": "GRANTED" or "DENIED",
    "reasoning": "Your summary",
    "roast": "Your one-liner",
    "jury_votes": {"skeptic": "REAL/FAKE", "doctor": "CRITICAL/STABLE", "gambler": "IN/OUT"}
}
"""
    
    try:
        # Run the Judge agent - it will orchestrate the jury
        print("⚖️ The Court is now in session...")
        response = pit_boss_judge(case_presentation)
        result_text = str(response)
        
        # Try to parse JSON from the response
        try:
            json_start = result_text.find('{')
            json_end = result_text.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                json_str = result_text[json_start:json_end]
                result = json.loads(json_str)
                # Remove door_code if present
                result.pop("door_code", None)
                return result
        except json.JSONDecodeError:
            pass
        
        # Fallback if JSON parsing fails
        return {
            "verdict": "DENIED",
            "reasoning": "The Court experienced technical difficulties during deliberation.",
            "roast": result_text[:200] if result_text else "The house always wins. Try again.",
            "jury_votes": {
                "skeptic": "UNKNOWN",
                "doctor": "UNKNOWN", 
                "gambler": "UNKNOWN"
            }
        }
        
    except Exception as e:
        print(f"❌ Court error: {e}")
        return {
            "verdict": "DENIED",
            "reasoning": f"Court error: {str(e)}",
            "roast": "Even the machines are against you today. House wins by default.",
            "jury_votes": {
                "skeptic": "ERROR",
                "doctor": "ERROR",
                "gambler": "ERROR"
            }
        }


# ============================================================================
# SIMPLE TEST
# ============================================================================

if __name__ == "__main__":
    print("Testing Court of Relief...")
    result = run_court_of_relief(
        user_plea="Please! I've been holding it for 3 hours! I'm about to explode!",
        demo_mode=False
    )
    print(json.dumps(result, indent=2))
