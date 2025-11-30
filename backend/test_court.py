#!/usr/bin/env python3
"""
Lucky Loo - Test Script
Quick tests for the Court of Relief

Usage:
    python test_court.py           # Run with mock mode
    python test_court.py --live    # Run with real AWS Bedrock (requires credentials)
"""

import sys
import json
import os

# Set mock mode for testing without AWS
if "--live" not in sys.argv:
    os.environ["MOCK_MODE"] = "true"

from agents import run_court_of_relief


def print_verdict(result: dict):
    """Pretty print a verdict."""
    verdict = result.get("verdict", "UNKNOWN")
    emoji = "✅" if verdict == "GRANTED" else "❌"
    
    print(f"""
{'='*60}
{emoji} VERDICT: {verdict}
{'='*60}

🎲 JURY VOTES:
   The Skeptic: {result.get('jury_votes', {}).get('skeptic', '?')}
   The Doctor:  {result.get('jury_votes', {}).get('doctor', '?')}
   The Gambler: {result.get('jury_votes', {}).get('gambler', '?')}

📋 REASONING:
   {result.get('reasoning', 'N/A')}

🎤 THE PIT BOSS SAYS:
   "{result.get('roast', 'No comment.')}"
""")
    
    if result.get("door_code"):
        print(f"🚪 DOOR CODE: {result.get('door_code')}")
    
    print("="*60)


def test_desperate_plea():
    """Test with a desperate plea."""
    print("\n🧪 TEST 1: Desperate Plea")
    print("-" * 40)
    
    result = run_court_of_relief(
        user_plea="PLEASE! I've been holding it for 4 hours! I'm about to EXPLODE! This is a medical emergency!!"
    )
    print_verdict(result)
    return result


def test_casual_plea():
    """Test with a casual, non-urgent plea."""
    print("\n🧪 TEST 2: Casual Plea")
    print("-" * 40)
    
    result = run_court_of_relief(
        user_plea="Hey, I kinda need to use the bathroom when you get a chance. No rush."
    )
    print_verdict(result)
    return result


def test_demo_mode():
    """Test demo mode (always wins)."""
    print("\n🧪 TEST 3: Demo Mode")
    print("-" * 40)
    
    result = run_court_of_relief(
        user_plea="Testing demo mode",
        demo_mode=True
    )
    print_verdict(result)
    assert result["verdict"] == "GRANTED", "Demo mode should always grant access"
    print("✅ Demo mode working correctly!")
    return result


def test_with_image_claim():
    """Test with a claim of image evidence."""
    print("\n🧪 TEST 4: With Image Claim")
    print("-" * 40)
    
    result = run_court_of_relief(
        user_plea="Look at my face! I'm dying here!",
        image_base64="fake_base64_image_data_here"  # In real use, this would be actual base64
    )
    print_verdict(result)
    return result


def main():
    print("""
    🎰 ══════════════════════════════════════════ 🎰
    
       LUCKY LOO - COURT OF RELIEF TEST SUITE
       
    🎰 ══════════════════════════════════════════ 🎰
    """)
    
    mode = "MOCK MODE" if os.getenv("MOCK_MODE") == "true" else "LIVE MODE (AWS Bedrock)"
    print(f"Running in: {mode}\n")
    
    # Run tests
    test_demo_mode()
    test_desperate_plea()
    test_casual_plea()
    test_with_image_claim()
    
    print("\n✅ All tests completed!")
    print("\nTo run with real AWS Bedrock, use: python test_court.py --live")


if __name__ == "__main__":
    main()

