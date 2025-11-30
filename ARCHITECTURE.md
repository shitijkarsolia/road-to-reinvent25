# 🏗️ Architecture Deep Dive

## The Agent Orchestration Pattern

```
                                USER SUBMITS PLEA
                                       ↓
                        ┌──────────────────────────┐
                        │   FastAPI Backend        │
                        │   /api/judge endpoint    │
                        └──────────────────────────┘
                                       ↓
                        ┌──────────────────────────┐
                        │  agents.py               │
                        │  run_court_of_relief()   │
                        └──────────────────────────┘
                                       ↓
           ┌───────────────────────────────────────────────┐
           │          AWS Bedrock                          │
           │       Claude Sonnet 4.5                       │
           │                                               │
           │   ┌───────────────────────────────────────┐  │
           │   │     THE PIT BOSS (Judge Agent)        │  │
           │   │                                       │  │
           │   │  System Prompt:                       │  │
           │   │  judge_pitboss.md                     │  │
           │   │                                       │  │
           │   │  Tools Available:                     │  │
           │   │  - consult_skeptic()                  │  │
           │   │  - consult_doctor()                   │  │
           │   │  - consult_gambler()                  │  │
           │   └───────────────────────────────────────┘  │
           │                      ↓                        │
           │        ┌─────────────┴─────────────┐         │
           │        ↓             ↓             ↓         │
           │   ┌─────────┐   ┌─────────┐   ┌─────────┐  │
           │   │ SKEPTIC │   │ DOCTOR  │   │ GAMBLER │  │
           │   │  Agent  │   │  Agent  │   │  Agent  │  │
           │   │         │   │         │   │         │  │
           │   │ Prompt: │   │ Prompt: │   │ Prompt: │  │
           │   │juror_   │   │juror_   │   │juror_   │  │
           │   │skeptic  │   │doctor   │   │gambler  │  │
           │   │   .md   │   │   .md   │   │   .md   │  │
           │   └─────────┘   └─────────┘   └─────────┘  │
           │        ↓             ↓             ↓         │
           │   "VERDICT:    "DIAGNOSIS:   "THE CARDS    │
           │    REAL"        CRITICAL"     SAY: IN"      │
           │                                               │
           └───────────────────────────────────────────────┘
                                       ↓
                        ┌──────────────────────────┐
                        │  Pit Boss Aggregates     │
                        │  Returns JSON:           │
                        │  {                       │
                        │    verdict: "GRANTED",   │
                        │    reasoning: "...",     │
                        │    roast: "...",         │
                        │    jury_votes: {...}     │
                        │  }                       │
                        └──────────────────────────┘
                                       ↓
                        ┌──────────────────────────┐
                        │   React Frontend         │
                        │   Displays Verdict       │
                        └──────────────────────────┘
```

---

## Agent Implementation in Code

### Step 1: Define Each Agent

**File: `backend/agents.py`**

```python
from strands import Agent
from strands.models import BedrockModel

# Initialize the model
bedrock_model = BedrockModel(
    model_id="us.anthropic.claude-sonnet-4-5-20250929-v1:0",
    region_name="us-east-1"
)

# Create each jury agent with their personality
juror_skeptic = Agent(
    name="The_Skeptic",
    model=bedrock_model,
    system_prompt=load_steering_prompt("juror_skeptic.md")
)

juror_doctor = Agent(
    name="The_Doctor",
    model=bedrock_model,
    system_prompt=load_steering_prompt("juror_doctor.md")
)

juror_gambler = Agent(
    name="The_Gambler",
    model=bedrock_model,
    system_prompt=load_steering_prompt("juror_gambler.md")
)
```

### Step 2: Wrap Agents as Tools

The Pit Boss needs to be able to "call" each jury member:

```python
from strands import tool

@tool
def consult_skeptic(face_analysis: str) -> str:
    """
    Consult The Skeptic with face analysis.
    The Pit Boss will call this function.
    """
    prompt = f"Analyze this evidence: {face_analysis}"
    response = juror_skeptic(prompt)  # Agent executes
    return str(response)

@tool
def consult_doctor(user_plea: str) -> str:
    """Consult The Doctor with the user's plea."""
    prompt = f"A patient says: '{user_plea}'"
    response = juror_doctor(prompt)
    return str(response)

@tool
def consult_gambler() -> str:
    """Consult The Gambler for luck factor."""
    prompt = "Should they get in? Check their luck."
    response = juror_gambler(prompt)
    return str(response)
```

### Step 3: Create the Orchestrator (Pit Boss)

The Pit Boss has access to all jury agents as tools:

```python
pit_boss_judge = Agent(
    name="Pit_Boss",
    model=bedrock_model,
    tools=[consult_skeptic, consult_doctor, consult_gambler],
    system_prompt=load_steering_prompt("judge_pitboss.md")
)
```

### Step 4: Run the Deliberation

```python
def run_court_of_relief(user_plea: str, image_base64: str = None):
    # Analyze face if image provided
    if image_base64:
        face_analysis = analyze_face_with_vision(image_base64)
    else:
        face_analysis = "No photo provided"
    
    # Build case presentation for the Judge
    case = f"""
    USER'S PLEA: "{user_plea}"
    FACE ANALYSIS: {face_analysis}
    
    Your task:
    1. Call consult_skeptic with the face analysis
    2. Call consult_doctor with the plea
    3. Call consult_gambler for luck
    4. Deliver your verdict as JSON
    """
    
    # The Pit Boss orchestrates everything
    response = pit_boss_judge(case)
    
    # Parse and return the verdict
    return parse_json_verdict(response)
```

---

## What Happens When Pit Boss Runs?

When you call `pit_boss_judge(case)`, here's what happens:

1. **Pit Boss reads the case presentation**
   - Sees the user's plea
   - Sees the face analysis (or lack of)
   - Sees instructions to consult the jury

2. **Pit Boss decides to call tools** (Strands handles this automatically)
   ```
   Pit Boss thinks: "I need to consult the jury..."
   → Calls consult_skeptic(face_analysis)
   → Waits for response
   → Calls consult_doctor(user_plea)
   → Waits for response
   → Calls consult_gambler()
   → Waits for response
   ```

3. **Each tool call triggers an agent execution**
   - `consult_skeptic()` → runs `juror_skeptic` agent
   - `consult_doctor()` → runs `juror_doctor` agent
   - `consult_gambler()` → runs `juror_gambler` agent

4. **Pit Boss receives all responses**
   - Skeptic: "VERDICT: FAKE..."
   - Doctor: "DIAGNOSIS: STABLE..."
   - Gambler: "THE CARDS SAY: OUT..."

5. **Pit Boss aggregates and decides**
   - Reads all jury opinions
   - Weighs them according to its prompt
   - Generates final verdict
   - Returns structured JSON

---

## The Vision Integration

**File: `backend/agents.py` → `analyze_face_with_vision()`**

```python
def analyze_face_with_vision(image_base64: str) -> dict:
    """
    Calls Claude Vision API directly (not through Strands)
    to analyze the user's facial expression.
    """
    
    # Build message with image
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
                "text": "Analyze this face for desperation..."
            }
        ]
    }
    
    # Call Bedrock directly via boto3
    response = bedrock_runtime.invoke_model(
        modelId=MODEL_ID,
        body=json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 300,
            "messages": [message]
        })
    )
    
    # Parse response
    result = json.loads(response["body"].read())
    analysis_text = result["content"][0]["text"]
    
    return {
        "verdict": "REAL" or "FAKE",
        "analysis": analysis_text
    }
```

This vision analysis result is then passed to The Skeptic for judgment.

---

## The Prompt Files

### `backend/steering/judge_pitboss.md`

The orchestrator's personality and instructions:

```markdown
You are The Pit Boss, the ultimate authority at Lucky Loo Casino.

Your task:
1. Call consult_skeptic with the face analysis
2. Call consult_doctor with the plea
3. Call consult_gambler for luck
4. Weigh their opinions
5. Deliver verdict as JSON

Rules:
- If Skeptic says FAKE → lean towards DENIED
- If Doctor says CRITICAL → lean towards GRANTED
- If Gambler says OUT → tiebreaker goes to DENIED

Output format:
{
    "verdict": "GRANTED" or "DENIED",
    "reasoning": "...",
    "roast": "Your one-liner",
    "jury_votes": {...}
}
```

### `backend/steering/juror_skeptic.md`

The Skeptic's personality:

```markdown
You are The Skeptic, a cynical Vegas bouncer.

Analyze faces for FAKE vs REAL desperation:
- FAKE: Smiling, relaxed, "acting"
- REAL: Genuine fear, sweat, tension

Output format:
VERDICT: [REAL/FAKE]
CONFIDENCE: [HIGH/MEDIUM/LOW]
REASONING: [Your noir-style analysis]
```

(Similar for Doctor and Gambler)

---

## API Endpoints

**File: `backend/app.py`**

```python
@app.post("/api/judge")
async def submit_plea(request: PleaRequest):
    """
    Receives: { plea: str, image_base64: str, demo_mode: bool }
    Returns: { verdict, reasoning, roast, jury_votes }
    """
    result = run_court_of_relief(
        user_plea=request.plea,
        image_base64=request.image_base64,
        demo_mode=request.demo_mode
    )
    return VerdictResponse(**result)
```

---

## Frontend State Machine

**File: `frontend/src/App.jsx`**

```javascript
const [stage, setStage] = useState('welcome')

// Stages:
// 1. 'welcome'     → Show intro, jury preview
// 2. 'camera'      → Capture webcam photo
// 3. 'plea'        → Write text plea
// 4. 'deliberating' → Show loading + jury thinking
// 5. 'verdict'     → Display final result

const submit = async () => {
    setStage('deliberating')
    
    const response = await fetch('/api/judge', {
        method: 'POST',
        body: JSON.stringify({ plea, image_base64, demo_mode })
    })
    
    const verdict = await response.json()
    setVerdict(verdict)
    setStage('verdict')
}
```

---

## Data Flow Summary

```
┌──────────────┐
│   Browser    │  User captures photo + writes plea
└──────┬───────┘
       │ HTTP POST /api/judge
       ↓
┌──────────────┐
│   FastAPI    │  Receives request
└──────┬───────┘
       │ Calls run_court_of_relief()
       ↓
┌──────────────┐
│  agents.py   │  Vision analysis (if image)
└──────┬───────┘
       │ Calls pit_boss_judge(case)
       ↓
┌──────────────────────────────────────┐
│  AWS Bedrock (Strands Orchestration) │
│                                      │
│  Pit Boss → consult_skeptic()        │
│          → consult_doctor()          │
│          → consult_gambler()         │
│                                      │
│  Each tool call runs a jury agent    │
│  Pit Boss aggregates responses       │
└──────┬───────────────────────────────┘
       │ Returns JSON verdict
       ↓
┌──────────────┐
│  FastAPI     │  Formats response
└──────┬───────┘
       │ HTTP Response
       ↓
┌──────────────┐
│   Browser    │  Displays verdict + jury votes
└──────────────┘
```

---

## Key Concepts

### 1. Agents-as-Tools Pattern
Each agent is wrapped as a `@tool` that another agent can call.

### 2. Hierarchical Delegation
Parent agent (Pit Boss) delegates tasks to child agents (Jury).

### 3. Vision Integration
Claude Vision API analyzes images before passing results to agents.

### 4. Personality Prompting
Each agent has a distinct character defined in markdown files.

### 5. JSON Structured Output
Final verdict is forced into JSON format for easy parsing.

---

For quick commands, see `QUICKSTART.md`  
For full docs, see `README.md`

