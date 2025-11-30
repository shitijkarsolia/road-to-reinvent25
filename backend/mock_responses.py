"""
Lucky Loo - Mock Responses
For testing without AWS credentials or when Bedrock is unavailable.
"""

import random

# Pre-written jury responses for offline testing
MOCK_SKEPTIC_RESPONSES = {
    "real": [
        """VERDICT: REAL
CONFIDENCE: HIGH
REASONING: Those eyes don't lie. I've seen that look a thousand times at the Bellagio buffet aftermath. This one's genuine.""",
        """VERDICT: REAL  
CONFIDENCE: MEDIUM
REASONING: Something in the way they're clenching their jaw... I've been doing this too long to be fooled. They're hurting.""",
    ],
    "fake": [
        """VERDICT: FAKE
CONFIDENCE: HIGH
REASONING: Nice try, sweetheart. That smile says 'Instagram photo op,' not 'bathroom emergency.' I wasn't born yesterday.""",
        """VERDICT: FAKE
CONFIDENCE: MEDIUM  
REASONING: Twenty years on The Strip, and I know a bluff when I see one. Those relaxed shoulders scream 'I'm fine.'""",
    ]
}

MOCK_DOCTOR_RESPONSES = {
    "critical": [
        """DIAGNOSIS: Acute Vesicular Hyperpressure Syndrome (AVHS)
URGENCY: CRITICAL
RECOMMENDATION: Grant access
MEDICAL OPINION: The patient exhibits textbook Stage 4 Bladder Rebellion. Delay could result in... *dramatic pause* ...catastrophic public humiliation.""",
        """DIAGNOSIS: Terminal Sphincter Fatigue with Secondary Urgency Cascade
URGENCY: CRITICAL
RECOMMENDATION: Grant access
MEDICAL OPINION: I've seen this before in my years at Vegas General. The desperation markers are off the charts. This is a CODE BROWN situation.""",
    ],
    "stable": [
        """DIAGNOSIS: Mild Inconvenience Syndrome
URGENCY: STABLE
RECOMMENDATION: Deny access
MEDICAL OPINION: The patient shows no signs of genuine distress. Vital signs are stable. They can hold it.""",
        """DIAGNOSIS: Attention-Seeking Bladder Dramatics (ASBD)
URGENCY: STABLE
RECOMMENDATION: Deny access  
MEDICAL OPINION: This is a textbook case of exaggeration. No medical intervention required.""",
    ]
}

MOCK_GAMBLER_RESPONSES = {
    "in": [
        """THE CARDS SAY: LET THEM IN
LUCKY NUMBER: 7
GAMBLER'S WISDOM: I just felt a hot streak coming on. When Lady Luck whispers, you listen. Today's their day.""",
        """THE CARDS SAY: LET THEM IN
LUCKY NUMBER: 21
GAMBLER'S WISDOM: Natural blackjack energy in the room. The cosmic dice have spoken. Let 'em through.""",
    ],
    "out": [
        """THE CARDS SAY: SEND THEM PACKING
LUCKY NUMBER: 13
GAMBLER'S WISDOM: Snake eyes. Double zeros. The house always wins, and right now, the house says no.""",
        """THE CARDS SAY: SEND THEM PACKING
LUCKY NUMBER: 4
GAMBLER'S WISDOM: Bad juju in the air tonight. Mercury's in retrograde. Can't risk it.""",
    ]
}

MOCK_VERDICTS = {
    "granted": {
        "verdict": "GRANTED",
        "door_code": "777",
        "reasoning": "The Skeptic detected genuine terror. The Doctor diagnosed critical bladder failure. The Gambler's dice rolled lucky sevens.",
        "roast": "Jackpot, kid. The Porcelain Gods smile upon you today. Door code: 777. Don't make me regret this.",
        "jury_votes": {
            "skeptic": "REAL",
            "doctor": "CRITICAL",
            "gambler": "IN"
        }
    },
    "denied": {
        "verdict": "DENIED",
        "door_code": None,
        "reasoning": "The Skeptic saw through your act. The Doctor says you'll live. The Gambler drew snake eyes on your behalf.",
        "roast": "House wins, tourist. Find a Starbucks and buy a coffee like everyone else. This ain't your lucky day.",
        "jury_votes": {
            "skeptic": "FAKE",
            "doctor": "STABLE",
            "gambler": "OUT"
        }
    }
}


def get_mock_response(force_win: bool = None) -> dict:
    """
    Get a mock response for testing.
    
    Args:
        force_win: If True, always return GRANTED. If False, always return DENIED.
                  If None, randomly choose.
    """
    if force_win is True:
        return MOCK_VERDICTS["granted"].copy()
    elif force_win is False:
        return MOCK_VERDICTS["denied"].copy()
    else:
        # Random with 50/50 odds
        return random.choice([
            MOCK_VERDICTS["granted"].copy(),
            MOCK_VERDICTS["denied"].copy()
        ])


def get_mock_jury_response(juror: str, favorable: bool = None) -> str:
    """Get a mock response from a specific juror."""
    if juror == "skeptic":
        if favorable is True:
            return random.choice(MOCK_SKEPTIC_RESPONSES["real"])
        elif favorable is False:
            return random.choice(MOCK_SKEPTIC_RESPONSES["fake"])
        else:
            return random.choice(
                MOCK_SKEPTIC_RESPONSES["real"] + MOCK_SKEPTIC_RESPONSES["fake"]
            )
    
    elif juror == "doctor":
        if favorable is True:
            return random.choice(MOCK_DOCTOR_RESPONSES["critical"])
        elif favorable is False:
            return random.choice(MOCK_DOCTOR_RESPONSES["stable"])
        else:
            return random.choice(
                MOCK_DOCTOR_RESPONSES["critical"] + MOCK_DOCTOR_RESPONSES["stable"]
            )
    
    elif juror == "gambler":
        if favorable is True:
            return random.choice(MOCK_GAMBLER_RESPONSES["in"])
        elif favorable is False:
            return random.choice(MOCK_GAMBLER_RESPONSES["out"])
        else:
            return random.choice(
                MOCK_GAMBLER_RESPONSES["in"] + MOCK_GAMBLER_RESPONSES["out"]
            )
    
    return "Unknown juror"

