# 🚀 Quick Start Guide

## Run Backend (Terminal 1)

```bash
cd /home/ubuntu/yellow/backend
source venv/bin/activate
python -m uvicorn app:app --host 0.0.0.0 --port 8000
```

**You should see:**
```
🎰 Using model: us.anthropic.claude-sonnet-4-5-20250929-v1:0
🌎 Region: us-east-1
🚽 Lucky Loo Court of Relief is now in session!
INFO: Uvicorn running on http://0.0.0.0:8000
```

## Run Frontend (Terminal 2)

```bash
cd /home/ubuntu/yellow/frontend
npm run dev
```

**You should see:**
```
VITE v5.x.x ready in xxx ms
➜ Local:   http://localhost:3000/
```

## Open In Browser

Navigate to: **http://localhost:3000**

---

## Currently Running

Both services should already be running in background terminals:
- Backend: Check terminal `/home/ubuntu/.cursor/projects/home-ubuntu-yellow/terminals/8.txt`
- Frontend: Check terminal `/home/ubuntu/.cursor/projects/home-ubuntu-yellow/terminals/5.txt`

To view running processes:
```bash
# Check if backend is running
lsof -i :8000

# Check if frontend is running
lsof -i :3000
```

---

## Test Backend Directly

```bash
# Health check
curl http://localhost:8000/

# Submit a test plea
curl -X POST http://localhost:8000/api/judge \
  -H "Content-Type: application/json" \
  -d '{
    "plea": "HELP! I have been holding it for 3 hours!!",
    "demo_mode": false
  }'
```

---

## How It Works (5-Second Version)

1. **User submits face photo + plea** → Frontend sends to `/api/judge`
2. **Backend calls Claude Vision** → Analyzes face for desperation
3. **Pit Boss orchestrates 3 jury agents**:
   - Skeptic (analyzes face)
   - Doctor (evaluates plea)
   - Gambler (random luck)
4. **Pit Boss aggregates votes** → Returns GRANTED/DENIED verdict
5. **Frontend displays result** with jury votes

---

## Key Files To Know

```
backend/agents.py          ← Agent orchestration logic
backend/app.py             ← API endpoints
backend/steering/*.md      ← Agent personality prompts
frontend/src/App.jsx       ← React UI
backend/.env               ← AWS config (model ID, region)
```

---

## Environment Variables

Located in `backend/.env`:
```bash
AWS_REGION=us-east-1
BEDROCK_MODEL_ID=us.anthropic.claude-sonnet-4-5-20250929-v1:0
PORT=8000
```

AWS credentials are handled by EC2 IAM role (no keys needed).

---

## Troubleshooting

**Backend error: "Model not found"**
→ Enable Claude Sonnet 4.5 in AWS Bedrock console

**Frontend can't reach backend**
→ Check backend is running on port 8000
→ Check proxy config in `frontend/vite.config.js`

**Vision not working**
→ Verify Claude model ID starts with "anthropic"
→ Check IAM permissions for `bedrock:InvokeModel`

---

For full documentation, see `README.md`

