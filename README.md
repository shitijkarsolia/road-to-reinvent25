# 🚽 Lucky Loo - The High-Stakes Restroom Finder

A "delightfully impractical" hackathon project that uses AWS Bedrock AI agents to judge whether you deserve bathroom access.

## 🎯 What Is This?

Lucky Loo is an AI-powered "Court of Relief" where you must prove your desperation to a jury of AI agents:
- **The Skeptic** 🕵️ - Analyzes your face photo using Claude Vision
- **The Doctor** 👨‍⚕️ - Evaluates your written plea for medical urgency
- **The Gambler** 🎲 - Decides your fate based on pure luck

The **Pit Boss** (Judge) orchestrates all three agents and delivers the final verdict: GRANTED or DENIED.

---

## Demo
https://github.com/user-attachments/assets/530e1075-2d40-4e7e-9bdd-ef8f043a0a92



## 🏗️ Architecture

### The Flow

```
User submits plea + optional face photo
          ↓
    FastAPI Backend receives request
          ↓
    agents.py → run_court_of_relief()
          ↓
┌─────────────────────────────────────┐
│   AWS Bedrock Claude Sonnet 4.5     │
│                                     │
│  ┌────────────────────────────┐    │
│  │  The Pit Boss (Judge)      │    │
│  │  Orchestrates the jury     │    │
│  └────────────────────────────┘    │
│              ↓                      │
│  ┌─────────┬─────────┬─────────┐  │
│  │ Skeptic │ Doctor  │ Gambler │  │
│  │  Agent  │  Agent  │  Agent  │  │
│  └─────────┴─────────┴─────────┘  │
│                                     │
└─────────────────────────────────────┘
          ↓
    JSON verdict returned
          ↓
    React frontend displays result
```

---

## 🧠 How The Agents Work

### Multi-Agent Pattern: "Agents-as-Tools"

This project uses **AWS Strands Agents** with the "Agents-as-Tools" pattern:

1. **Parent Agent (Pit Boss)** has child agents registered as tools
2. When the Pit Boss runs, it decides which tools (agents) to call
3. Each jury agent has its own personality and decision logic
4. The Pit Boss aggregates all responses and delivers final verdict

### Where The Prompts Are

All agent personalities are defined in **markdown files**:

```
backend/steering/
├── judge_pitboss.md    ← The orchestrator
├── juror_skeptic.md    ← Analyzes faces
├── juror_doctor.md     ← Evaluates pleas
└── juror_gambler.md    ← Pure chaos
```

These prompts are loaded in `backend/agents.py`:

```python
juror_skeptic = Agent(
    name="The_Skeptic",
    model=bedrock_model,
    system_prompt=load_steering_prompt("juror_skeptic.md"),
)
```

### The Agent Tools

Each jury member is wrapped as a `@tool` that the Pit Boss can call:

```python
@tool
def consult_skeptic(face_analysis: str) -> str:
    """The Pit Boss calls this to consult The Skeptic"""
    response = juror_skeptic(prompt)
    return str(response)
```

The Pit Boss agent has these tools registered:

```python
pit_boss_judge = Agent(
    name="Pit_Boss",
    model=bedrock_model,
    tools=[consult_skeptic, consult_doctor, consult_gambler],
    system_prompt=load_steering_prompt("judge_pitboss.md"),
)
```

---

## 📸 How Vision Works

When a user submits a face photo:

1. **Frontend** captures webcam image, converts to base64
2. **Backend** receives base64 image
3. `analyze_face_with_vision()` calls **Claude Vision API** directly via boto3
4. Claude analyzes the face for signs of desperation
5. Result is passed to The Skeptic agent
6. Skeptic uses this analysis to make their verdict

Code location: `backend/agents.py` → `analyze_face_with_vision()`

---

## 🚀 How To Run

### Backend (Port 8000)

```bash
# Navigate to backend
cd /home/ubuntu/yellow/backend

# Activate virtual environment
source venv/bin/activate

# Make sure .env exists with AWS config
cat .env
# Should contain:
# AWS_REGION=us-east-1
# BEDROCK_MODEL_ID=us.anthropic.claude-sonnet-4-5-20250929-v1:0
# PORT=8000

# Run the server
python -m uvicorn app:app --host 0.0.0.0 --port 8000

# Or with auto-reload for development
python -m uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

The backend will start at **http://localhost:8000**

### Frontend (Port 3000)

```bash
# Navigate to frontend (in a new terminal)
cd /home/ubuntu/yellow/frontend

# Run the dev server
npm run dev
```

The frontend will start at **http://localhost:3000**

### Testing Without Frontend

You can test the backend API directly:

```bash
# Health check
curl http://localhost:8000/api/health

# Submit a plea (no image)
curl -X POST http://localhost:8000/api/judge \
  -H "Content-Type: application/json" \
  -d '{"plea": "PLEASE! I am about to explode!!", "demo_mode": false}'

# Demo mode (always wins)
curl -X POST http://localhost:8000/api/demo
```

---

## 📁 Project Structure

```
yellow/
├── backend/                    # Python FastAPI backend
│   ├── agents.py              # Main agent logic & orchestration
│   ├── app.py                 # FastAPI endpoints
│   ├── mock_responses.py      # Mock data for testing
│   ├── vision.py              # Claude vision integration
│   ├── requirements.txt       # Python dependencies
│   ├── .env                   # AWS credentials (not in git)
│   └── steering/              # Agent personality prompts
│       ├── judge_pitboss.md   # Judge orchestrator prompt
│       ├── juror_skeptic.md   # Skeptic personality
│       ├── juror_doctor.md    # Doctor personality
│       └── juror_gambler.md   # Gambler personality
│
├── frontend/                  # React + Vite frontend
│   ├── src/
│   │   ├── App.jsx           # Main React component
│   │   ├── index.css         # Tailwind + custom styles
│   │   └── main.jsx          # React entry point
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
│
└── docs/                      # Project documentation
    ├── details.md             # Original hackathon spec
    ├── jury.md                # Jury system design
    └── Task.md                # Implementation tasks
```

---

## 🔑 Key Files Explained

### `backend/agents.py`
The brain of the operation. Contains:
- Agent definitions (Skeptic, Doctor, Gambler, Pit Boss)
- Tool wrappers for each agent
- `run_court_of_relief()` - main function that runs the full deliberation
- Vision analysis integration

### `backend/app.py`
FastAPI server with endpoints:
- `POST /api/judge` - Submit plea for judgment
- `POST /api/judge/upload` - Submit with file upload
- `POST /api/demo` - Demo mode (always wins)
- `GET /api/health` - Health check

### `frontend/src/App.jsx`
React component with stages:
1. **Welcome** - Explains the concept
2. **Camera** - Capture face photo (optional)
3. **Plea** - Write your desperate plea
4. **Deliberating** - Animated jury thinking
5. **Verdict** - Final result with jury votes

---

## 🔄 The Complete Request Flow

1. **User clicks "I Need To Go"** → Stage: Camera
2. **User captures photo** → Image converted to base64
3. **User writes plea** → Both stored in state
4. **User submits** → 
   ```javascript
   fetch('/api/judge', {
     method: 'POST',
     body: JSON.stringify({ plea, image_base64, demo_mode })
   })
   ```

5. **Backend receives request** → `app.py:submit_plea()`
6. **Calls agent system** → `agents.py:run_court_of_relief()`
7. **Vision analysis** (if image provided):
   ```python
   analyze_face_with_vision(image_base64)
   # Returns: {"verdict": "REAL/FAKE", "analysis": "..."}
   ```

8. **Pit Boss orchestration**:
   ```python
   pit_boss_judge(case_presentation)
   # Pit Boss internally calls:
   #   - consult_skeptic(face_analysis)
   #   - consult_doctor(plea)
   #   - consult_gambler()
   ```

9. **Each tool call triggers an agent**:
   - Skeptic analyzes face evidence
   - Doctor evaluates plea text
   - Gambler makes random decision

10. **Pit Boss aggregates votes**:
    - Weighs jury opinions
    - Delivers final verdict
    - Returns JSON response

11. **Frontend receives verdict**:
    ```json
    {
      "verdict": "GRANTED" or "DENIED",
      "reasoning": "...",
      "roast": "The Pit Boss's one-liner",
      "jury_votes": {
        "skeptic": "REAL/FAKE",
        "doctor": "CRITICAL/STABLE",
        "gambler": "IN/OUT"
      }
    }
    ```

12. **UI displays result** with confetti or shake animation

---

## 🎨 UI Components

### Jury Cards
Each jury member has a card showing:
- Emoji icon
- Name
- Status (Thinking... / Vote)
- Color-coded border (green=yes, red=no)

### Slot Machine
Visual feedback during deliberation and verdict:
- Spinning: 🎰 🎰 🎰
- Granted: ✅ ✅ ✅
- Denied: ❌ ❌ ❌

### Animations
- **fade-in** - Smooth entry for each stage
- **shake** - Screen shake on denial
- **Confetti** - Celebration on granted

---

## 🐛 Troubleshooting

### Backend won't start
```bash
# Check if port 8000 is in use
lsof -i :8000
# Kill if needed
kill -9 <PID>

# Check AWS credentials
aws sts get-caller-identity

# Check environment variables
cd backend && cat .env
```

### Frontend won't connect to backend
```bash
# Check proxy config in frontend/vite.config.js
# Should have:
proxy: {
  '/api': {
    target: 'http://localhost:8000',
    changeOrigin: true,
  }
}
```

### Agents returning errors
```bash
# Check backend logs in terminal
# Look for:
# - "🎰 Using model: us.anthropic.claude-sonnet-4-5..."
# - "⚖️ The Court is now in session..."
# - "👁️ Analyzing face with Claude Vision..."

# Test Bedrock access
aws bedrock list-foundation-models --region us-east-1
```

---

## 🧪 Demo Mode

For stage presentations, enable Demo Mode:
- Check the "Demo Mode" checkbox in UI
- Always returns "GRANTED" verdict
- Skips all AI calls (instant response)

---

## 🔐 AWS Requirements

You need:
1. **AWS Account** with IAM credentials on EC2
2. **Bedrock Model Access** - Enable Claude Sonnet 4.5 in AWS Console
3. **IAM Permissions**:
   - `bedrock:InvokeModel`
   - `bedrock:InvokeModelWithResponseStream`

---

## 📝 Customization

### Change Agent Personalities
Edit the markdown files in `backend/steering/`:
- Make agents meaner/nicer
- Add new decision criteria
- Change output format

### Add New Jury Members
1. Create new steering prompt: `backend/steering/juror_newrole.md`
2. Define agent in `agents.py`
3. Wrap as `@tool`
4. Add to Pit Boss tools list
5. Update frontend `JURY` array in `App.jsx`

### Change AI Model
Edit `backend/.env`:
```bash
# Switch to different Claude model
BEDROCK_MODEL_ID=anthropic.claude-3-opus-20240229-v1:0

# Or use Llama (cheaper, no vision)
BEDROCK_MODEL_ID=us.meta.llama3-3-70b-instruct-v1:0
```

---

## 🎬 Tech Stack

- **Frontend**: React 18 + Vite 5 + Tailwind CSS
- **Backend**: Python 3.11 + FastAPI + Uvicorn
- **AI**: AWS Bedrock (Claude Sonnet 4.5) + Strands Agents SDK
- **Vision**: Claude Vision API via boto3
- **Deployment**: EC2 (with IAM role for AWS access)

---

## 🏆 Credits

Built for the AWS hackathon "Road to re:Invent"
- Uses cutting-edge **Strands Agents** (open source multi-agent SDK)
- Demonstrates **Agents-as-Tools** pattern
- Showcases **Claude Vision** capabilities
- Fully serverless-ready architecture

---

## 📄 License

MIT License - Feel free to use for your own hackathons!

*"Because in Vegas, even a flush is a gamble." 🎰*
