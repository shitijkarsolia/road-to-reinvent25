# 🤝 Sharing Your Backend API

Quick guide for sharing your Lucky Loo backend with frontend developers.

---

## 1️⃣ Get Your API URL

### If running on EC2:

```bash
# Get your public IP
curl -s http://checkip.amazonaws.com

# Your API URL will be:
# http://YOUR_IP:8000
```

### If running locally:

```bash
# Your API URL will be:
# http://localhost:8000
```

---

## 2️⃣ Ensure Port 8000 is Open

### EC2 Security Group Settings:

1. Go to AWS Console → EC2 → Security Groups
2. Find your instance's security group
3. Add inbound rule:
   - **Type:** Custom TCP
   - **Port:** 8000
   - **Source:** 0.0.0.0/0 (or specific IP for security)

---

## 3️⃣ Share These Files

Send your frontend developer:

1. **`API_DOCS.md`** ← Complete API documentation
2. **Your API URL** → `http://YOUR_EC2_IP:8000`

That's it! They have everything they need.

---

## 4️⃣ Quick Test Commands

Give them these to verify the API works:

```bash
# Replace YOUR_EC2_IP with your actual IP

# 1. Health check
curl http://YOUR_EC2_IP:8000/api/health

# 2. Quick demo
curl -X POST http://YOUR_EC2_IP:8000/api/demo

# 3. Real test (no image)
curl -X POST http://YOUR_EC2_IP:8000/api/judge \
  -H "Content-Type: application/json" \
  -d '{"plea": "HELP ME!", "demo_mode": false}'
```

---

## 5️⃣ What They Need to Know

### ✅ Key Points:

- **Base URL:** `http://YOUR_EC2_IP:8000`
- **Main Endpoint:** `POST /api/judge`
- **No Authentication:** Open API
- **CORS:** Enabled for all origins
- **Response Time:** 5-10 seconds (AI processing)
- **Demo Mode:** Available at `POST /api/demo` (instant response)

### 📋 Request Format:

```javascript
{
  "plea": "string (required)",
  "image_base64": "string (optional)",
  "demo_mode": boolean (optional)
}
```

### 📋 Response Format:

```javascript
{
  "verdict": "GRANTED" or "DENIED",
  "reasoning": "string",
  "roast": "string",
  "jury_votes": {
    "skeptic": "REAL" or "FAKE",
    "doctor": "CRITICAL" or "STABLE",
    "gambler": "IN" or "OUT"
  }
}
```

---

## 6️⃣ Example Frontend Integration

### React:

```jsx
const [verdict, setVerdict] = useState(null);

const submitPlea = async (plea, imageBase64 = null) => {
  const response = await fetch('http://YOUR_EC2_IP:8000/api/judge', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      plea: plea,
      image_base64: imageBase64,
      demo_mode: false
    })
  });
  
  const data = await response.json();
  setVerdict(data);
};
```

### Vanilla JavaScript:

```javascript
fetch('http://YOUR_EC2_IP:8000/api/judge', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    plea: 'HELP! Emergency!',
    demo_mode: false
  })
})
.then(res => res.json())
.then(data => {
  console.log('Verdict:', data.verdict);
  console.log('Roast:', data.roast);
  console.log('Jury votes:', data.jury_votes);
});
```

---

## 7️⃣ Common Issues

### CORS Error?
- ✅ Already handled - backend allows all origins

### Connection Refused?
- ❌ Check: Backend is running (`curl http://YOUR_EC2_IP:8000/api/health`)
- ❌ Check: Port 8000 is open in EC2 security group

### Timeout?
- ⏱️ Normal - AI takes 5-10 seconds
- ⏱️ Set fetch timeout to 30+ seconds
- 🎭 Use demo mode for instant testing

### 404 Not Found?
- ❌ Check: Using `/api/judge` not `/judge`
- ❌ Check: Backend is running

---

## 8️⃣ Keep Backend Running

### Option 1: Keep Terminal Open
```bash
cd /home/ubuntu/yellow/backend
source venv/bin/activate
python -m uvicorn app:app --host 0.0.0.0 --port 8000
```

### Option 2: Run in Background
```bash
cd /home/ubuntu/yellow/backend
source venv/bin/activate
nohup python -m uvicorn app:app --host 0.0.0.0 --port 8000 > server.log 2>&1 &

# View logs:
tail -f server.log
```

### Option 3: Use screen/tmux
```bash
# Start screen session
screen -S luckyloo

# Run backend
cd /home/ubuntu/yellow/backend
source venv/bin/activate
python -m uvicorn app:app --host 0.0.0.0 --port 8000

# Detach: Ctrl+A, then D
# Reattach: screen -r luckyloo
```

---

## ✅ Checklist for Frontend Developer

Share this checklist:

- [ ] I have the API URL: `http://YOUR_EC2_IP:8000`
- [ ] I can access `/api/health` and get `{"status":"healthy"}`
- [ ] I can POST to `/api/demo` and get a GRANTED response
- [ ] I understand the request/response format
- [ ] I know response time is 5-10 seconds
- [ ] I have set appropriate timeout in my code
- [ ] I show loading state to users

---

## 📞 Support

If they have issues:

1. **Test health:** `curl http://YOUR_EC2_IP:8000/api/health`
2. **Check backend logs:** Look at terminal where backend is running
3. **Try demo mode:** Should return instantly
4. **Verify security group:** Port 8000 must be open

---

**Your API is ready to share!** 🎉

Just send them:
1. `API_DOCS.md` file
2. Your EC2 IP address
3. Confirmation that backend is running

They can start integrating immediately!

