"""
Lucky Loo - Vision Analysis Module
Uses Claude 3's vision capabilities via Bedrock to analyze "desperation faces"
"""

import os
import json
import base64
import boto3
from typing import Optional


def analyze_desperation_face(
    image_base64: str,
    region: str = None
) -> dict:
    """
    Analyze a face image for signs of desperation using Claude 3 Vision.
    
    Args:
        image_base64: Base64-encoded image data
        region: AWS region (defaults to env var or us-east-1)
    
    Returns:
        dict with desperation analysis including:
        - is_desperate: bool
        - confidence: float (0-100)
        - emotions_detected: list of detected emotions
        - analysis: text description
    """
    region = region or os.getenv("AWS_REGION", "us-east-1")
    
    # Initialize Bedrock runtime client
    bedrock = boto3.client(
        service_name="bedrock-runtime",
        region_name=region
    )
    
    # Build the message with vision
    message = {
        "role": "user",
        "content": [
            {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": "image/jpeg",  # Adjust based on actual image type
                    "data": image_base64
                }
            },
            {
                "type": "text",
                "text": """You are analyzing a face for signs of BATHROOM DESPERATION.

Look for these indicators of GENUINE desperation:
- Wide, panicked eyes
- Clenched jaw or grimacing
- Sweat on forehead
- Pained expression
- Tense facial muscles
- Fear or distress in eyes

Look for these indicators of FAKE desperation:
- Relaxed expression trying to look distressed
- Smiling or laughing
- Calm, relaxed eyebrows
- No visible tension
- "Acting" rather than genuine distress

Respond with ONLY this JSON format (no other text):
{
    "is_desperate": true/false,
    "confidence": 0-100,
    "emotions_detected": ["list", "of", "emotions"],
    "physical_signs": ["list", "of", "observed", "signs"],
    "analysis": "Brief one-sentence assessment in a cynical Vegas bouncer tone"
}"""
            }
        ]
    }
    
    try:
        # Call Claude 3 Haiku with vision
        response = bedrock.invoke_model(
            modelId="anthropic.claude-3-haiku-20240307-v1:0",
            body=json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 500,
                "messages": [message]
            })
        )
        
        # Parse response
        result = json.loads(response["body"].read())
        content = result.get("content", [{}])[0].get("text", "{}")
        
        # Try to parse the JSON response
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            # If JSON parsing fails, return a default response
            return {
                "is_desperate": False,
                "confidence": 50,
                "emotions_detected": ["unknown"],
                "physical_signs": ["unable to analyze"],
                "analysis": "The image was unclear. Assuming you're faking it."
            }
            
    except Exception as e:
        print(f"Vision analysis error: {e}")
        return {
            "is_desperate": False,
            "confidence": 0,
            "emotions_detected": ["error"],
            "physical_signs": ["analysis_failed"],
            "analysis": f"Technical difficulties. Error: {str(e)}"
        }


def get_image_media_type(image_base64: str) -> str:
    """
    Detect image type from base64 data.
    """
    # Check for common image signatures
    if image_base64.startswith("/9j/"):
        return "image/jpeg"
    elif image_base64.startswith("iVBORw"):
        return "image/png"
    elif image_base64.startswith("R0lGOD"):
        return "image/gif"
    elif image_base64.startswith("UklGR"):
        return "image/webp"
    else:
        return "image/jpeg"  # Default to JPEG


# Mock response for testing without AWS
MOCK_VISION_RESPONSES = [
    {
        "is_desperate": True,
        "confidence": 92,
        "emotions_detected": ["fear", "distress", "urgency"],
        "physical_signs": ["wide eyes", "clenched jaw", "visible sweat"],
        "analysis": "Those eyes don't lie. This one's about to burst."
    },
    {
        "is_desperate": False,
        "confidence": 85,
        "emotions_detected": ["calm", "amusement"],
        "physical_signs": ["relaxed brow", "slight smile"],
        "analysis": "Nice try, but that smirk says 'Instagram content', not 'emergency'."
    }
]


def mock_analyze_face(force_desperate: bool = None) -> dict:
    """Mock vision analysis for testing."""
    import random
    
    if force_desperate is True:
        return MOCK_VISION_RESPONSES[0]
    elif force_desperate is False:
        return MOCK_VISION_RESPONSES[1]
    else:
        return random.choice(MOCK_VISION_RESPONSES)

