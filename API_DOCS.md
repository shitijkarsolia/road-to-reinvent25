# 🚽 Lucky Loo API Documentation

**Base URL:** `http://YOUR_EC2_IP:8000` or `http://localhost:8000` (if running locally)

**Version:** 1.0.0

---

## 📋 Overview

Lucky Loo is an AI-powered "Court of Relief" where users must prove their bathroom desperation to a jury of AI agents. This API processes user pleas (text + optional face photo) and returns verdicts from the AI jury.

### Key Features
- ✅ Text-based plea evaluation
- 📸 Optional face photo analysis (Claude Vision)
- 🤖 Multi-agent AI deliberation
- 🎭 Demo mode for testing

---

## 🔐 Authentication

**No authentication required.** The API is open for hackathon/demo purposes.

**CORS:** Enabled for all origins (`*`)

---

## 📡 Endpoints

### 1. Root - API Info

**GET /** 

Returns basic API information.

**Request:**
```bash
curl http://YOUR_EC2_IP:8000/
```

**Response:**
```json
{
    "name": "Lucky Loo - Court of Relief API",
    "tagline": "Because in Vegas, even a flush is a gamble.",
    "endpoints": {
        "health": "GET /api/health",
        "judge": "POST /api/judge",
        "judge_upload": "POST /api/judge/upload",
        "demo": "POST /api/demo"
    },
    "jury": [
        "The Skeptic",
        "The Doctor",
        "The Gambler"
    ],
    "judge": "The Pit Boss"
}
```

---

### 2. Health Check

**GET /api/health**

Check if the API is running.

**Request:**
```bash
curl http://YOUR_EC2_IP:8000/api/health
```

**Response:**
```json
{
    "status": "healthy",
    "service": "lucky-loo-court",
    "version": "1.0.0"
}
```

---

### 3. Submit Plea (JSON)

**POST /api/judge**

Submit a plea for bathroom access. This is the main endpoint.

**Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
    "plea": "PLEASE! I've been holding it for 3 hours! I'm about to EXPLODE!!",
    "image_base64": "base64_encoded_image_data_here",  // optional
    "demo_mode": false                                   // optional
}
```

**Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `plea` | string | ✅ Yes | User's desperate plea (min 3 chars) |
| `image_base64` | string | ❌ No | Base64-encoded JPEG image (without `data:image/jpeg;base64,` prefix) |
| `demo_mode` | boolean | ❌ No | If `true`, always returns GRANTED (for testing) |

**Example Request (No Image):**
```bash
curl -X POST http://YOUR_EC2_IP:8000/api/judge \
  -H "Content-Type: application/json" \
  -d '{
    "plea": "HELP! I drank 5 coffees and have been stuck in traffic for 4 hours! EMERGENCY!",
    "demo_mode": false
  }'
```

**Example Request (With Image):**
```bash
# First, convert image to base64 (no data URI prefix)
IMAGE_BASE64=$(base64 -w 0 photo.jpg)

curl -X POST http://YOUR_EC2_IP:8000/api/judge \
  -H "Content-Type: application/json" \
  -d "{
    \"plea\": \"Look at my face! I am DYING here!\",
    \"image_base64\": \"$IMAGE_BASE64\",
    \"demo_mode\": false
  }"
```

**Example JavaScript (Frontend):**
```javascript
// Capture image from webcam
const imageDataURL = webcamRef.current.getScreenshot();
const base64Image = imageDataURL.split(',')[1]; // Remove data:image/jpeg;base64, prefix

// Submit to API
const response = await fetch('http://YOUR_EC2_IP:8000/api/judge', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    plea: userPleaText,
    image_base64: base64Image,
    demo_mode: false
  })
});

const verdict = await response.json();
console.log(verdict);
```

**Response (GRANTED):**
```json
{
    "verdict": "GRANTED",
    "reasoning": "The Skeptic detected genuine terror in your face. The Doctor diagnosed critical bladder failure. The Gambler's dice rolled lucky sevens.",
    "roast": "Jackpot, kid. The Porcelain Gods smile upon you today. Make it quick.",
    "jury_votes": {
        "skeptic": "REAL",
        "doctor": "CRITICAL",
        "gambler": "IN"
    }
}
```

**Response (DENIED):**
```json
{
    "verdict": "DENIED",
    "reasoning": "The Skeptic saw through your act. The Doctor says you'll live. The Gambler drew snake eyes.",
    "roast": "House wins, tourist. Find a Starbucks. This ain't your lucky day.",
    "jury_votes": {
        "skeptic": "FAKE",
        "doctor": "STABLE",
        "gambler": "OUT"
    }
}
```

**Response Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `verdict` | string | `"GRANTED"` or `"DENIED"` |
| `reasoning` | string | Summary of jury deliberation |
| `roast` | string | The Pit Boss's one-liner (flavor text) |
| `jury_votes` | object | Individual votes from each jury member |
| `jury_votes.skeptic` | string | `"REAL"` (favor) or `"FAKE"` (against) |
| `jury_votes.doctor` | string | `"CRITICAL"` (favor) or `"STABLE"` (against) |
| `jury_votes.gambler` | string | `"IN"` (favor) or `"OUT"` (against) |

**Error Response (400):**
```json
{
    "detail": "Your plea must be at least 3 characters. The Court requires substance."
}
```

**Error Response (500):**
```json
{
    "detail": "The Court experienced an unexpected error: [error message]"
}
```

---

### 4. Submit Plea (Form Upload)

**POST /api/judge/upload**

Alternative endpoint that accepts multipart/form-data (useful for file uploads).

**Headers:**
```
Content-Type: multipart/form-data
```

**Form Fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `plea` | string | ✅ Yes | User's plea text |
| `demo_mode` | boolean | ❌ No | Demo mode flag |
| `image` | file | ❌ No | JPEG/PNG image file |

**Example Request:**
```bash
curl -X POST http://YOUR_EC2_IP:8000/api/judge/upload \
  -F "plea=HELP ME PLEASE!" \
  -F "demo_mode=false" \
  -F "image=@photo.jpg"
```

**Response:** Same as `/api/judge` endpoint

---

### 5. Demo Mode

**POST /api/demo**

Always returns a GRANTED verdict. Use for testing/presentations.

**Request:**
```bash
curl -X POST http://YOUR_EC2_IP:8000/api/demo
```

**Response:**
```json
{
    "verdict": "GRANTED",
    "reasoning": "DEMO MODE: The Court has been rigged in your favor.",
    "roast": "Jackpot! The Porcelain Gods recognize a VIP when they see one.",
    "jury_votes": {
        "skeptic": "REAL",
        "doctor": "CRITICAL",
        "gambler": "IN"
    }
}
```

---

## 🎨 Frontend Integration Guide

### Basic Flow

1. **User enters plea** → Capture text input
2. **Optional: Capture face photo** → Use webcam/camera
3. **Convert photo to base64** → Remove data URI prefix
4. **POST to `/api/judge`** → Send plea + image
5. **Display verdict** → Show result with jury votes

### React Example

```jsx
import { useState, useRef } from 'react';
import Webcam from 'react-webcam';

function BathroomFinder() {
  const [plea, setPlea] = useState('');
  const [verdict, setVerdict] = useState(null);
  const [loading, setLoading] = useState(false);
  const webcamRef = useRef(null);

  const captureAndSubmit = async () => {
    setLoading(true);
    
    // Capture image from webcam
    const imageSrc = webcamRef.current?.getScreenshot();
    const imageBase64 = imageSrc ? imageSrc.split(',')[1] : null;
    
    try {
      const response = await fetch('http://YOUR_EC2_IP:8000/api/judge', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          plea: plea,
          image_base64: imageBase64,
          demo_mode: false
        })
      });
      
      const data = await response.json();
      setVerdict(data);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <Webcam ref={webcamRef} />
      
      <textarea
        value={plea}
        onChange={(e) => setPlea(e.target.value)}
        placeholder="State your case..."
      />
      
      <button onClick={captureAndSubmit} disabled={loading}>
        {loading ? 'Deliberating...' : 'Submit to Court'}
      </button>
      
      {verdict && (
        <div>
          <h2>{verdict.verdict}</h2>
          <p>{verdict.roast}</p>
          <p>Skeptic: {verdict.jury_votes.skeptic}</p>
          <p>Doctor: {verdict.jury_votes.doctor}</p>
          <p>Gambler: {verdict.jury_votes.gambler}</p>
        </div>
      )}
    </div>
  );
}
```

### Vue Example

```vue
<template>
  <div>
    <video ref="video" autoplay></video>
    <canvas ref="canvas" style="display:none"></canvas>
    
    <textarea v-model="plea" placeholder="State your case..."></textarea>
    
    <button @click="submitPlea" :disabled="loading">
      {{ loading ? 'Deliberating...' : 'Submit to Court' }}
    </button>
    
    <div v-if="verdict">
      <h2>{{ verdict.verdict }}</h2>
      <p>{{ verdict.roast }}</p>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      plea: '',
      verdict: null,
      loading: false
    };
  },
  methods: {
    async captureImage() {
      const video = this.$refs.video;
      const canvas = this.$refs.canvas;
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      canvas.getContext('2d').drawImage(video, 0, 0);
      return canvas.toDataURL('image/jpeg').split(',')[1];
    },
    
    async submitPlea() {
      this.loading = true;
      const imageBase64 = await this.captureImage();
      
      try {
        const response = await fetch('http://YOUR_EC2_IP:8000/api/judge', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            plea: this.plea,
            image_base64: imageBase64,
            demo_mode: false
          })
        });
        
        this.verdict = await response.json();
      } catch (error) {
        console.error(error);
      } finally {
        this.loading = false;
      }
    }
  }
}
</script>
```

---

## ⏱️ Response Times

**Typical latency:**
- Demo mode: < 100ms (instant)
- Without image: 3-8 seconds (3 AI agent calls)
- With image: 5-10 seconds (vision analysis + 3 agent calls)

**Note:** First request after server start may take 10-15 seconds as agents initialize.

---

## 🎭 Understanding the Jury Votes

### The Skeptic
- **REAL** = Detected genuine desperation in face/text
- **FAKE** = Suspects you're faking it

### The Doctor  
- **CRITICAL** = Medical emergency detected
- **STABLE** = You can hold it

### The Gambler
- **IN** = Luck is on your side
- **OUT** = Snake eyes, better luck next time

**Verdict Logic:**
- 2+ favorable votes = GRANTED
- 2+ unfavorable votes = DENIED
- Pit Boss makes final call on ties

---

## 🐛 Error Handling

### Common Errors

**400 Bad Request - Plea too short**
```json
{
    "detail": "Your plea must be at least 3 characters. The Court requires substance."
}
```

**500 Internal Server Error - AI failure**
```json
{
    "detail": "The Court experienced an unexpected error: [details]"
}
```

**Connection timeout**
- Backend may take 5-10 seconds for AI response
- Set fetch timeout to at least 30 seconds
- Show loading indicator to user

### Recommended Error Handling

```javascript
try {
  const response = await fetch('http://YOUR_EC2_IP:8000/api/judge', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ plea, image_base64 }),
    signal: AbortSignal.timeout(30000) // 30 second timeout
  });
  
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Request failed');
  }
  
  const verdict = await response.json();
  return verdict;
  
} catch (error) {
  if (error.name === 'TimeoutError') {
    console.error('Request timed out - backend may be processing');
    // Show: "The Court is taking longer than usual..."
  } else {
    console.error('Error:', error.message);
  }
}
```

---

## 🧪 Testing the API

### Test with curl

```bash
# 1. Check health
curl http://YOUR_EC2_IP:8000/api/health

# 2. Test demo mode (instant)
curl -X POST http://YOUR_EC2_IP:8000/api/demo

# 3. Submit a plea (no image)
curl -X POST http://YOUR_EC2_IP:8000/api/judge \
  -H "Content-Type: application/json" \
  -d '{
    "plea": "EMERGENCY! I need help NOW!",
    "demo_mode": false
  }'

# 4. Submit with image
curl -X POST http://YOUR_EC2_IP:8000/api/judge/upload \
  -F "plea=Look at my face!" \
  -F "image=@desperate_face.jpg"
```

### Test with Postman

1. **Import this collection:**

```json
{
  "info": {
    "name": "Lucky Loo API",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Health Check",
      "request": {
        "method": "GET",
        "header": [],
        "url": {
          "raw": "http://YOUR_EC2_IP:8000/api/health",
          "protocol": "http",
          "host": ["YOUR_EC2_IP"],
          "port": "8000",
          "path": ["api", "health"]
        }
      }
    },
    {
      "name": "Submit Plea",
      "request": {
        "method": "POST",
        "header": [
          {
            "key": "Content-Type",
            "value": "application/json"
          }
        ],
        "body": {
          "mode": "raw",
          "raw": "{\n  \"plea\": \"PLEASE! I am about to explode!\",\n  \"demo_mode\": false\n}"
        },
        "url": {
          "raw": "http://YOUR_EC2_IP:8000/api/judge",
          "protocol": "http",
          "host": ["YOUR_EC2_IP"],
          "port": "8000",
          "path": ["api", "judge"]
        }
      }
    },
    {
      "name": "Demo Mode",
      "request": {
        "method": "POST",
        "header": [],
        "url": {
          "raw": "http://YOUR_EC2_IP:8000/api/demo",
          "protocol": "http",
          "host": ["YOUR_EC2_IP"],
          "port": "8000",
          "path": ["api", "demo"]
        }
      }
    }
  ]
}
```

---

## 📝 Best Practices

### 1. Image Handling
- ✅ Use JPEG format (best compression)
- ✅ Resize large images before sending (max 1MB recommended)
- ✅ Remove `data:image/jpeg;base64,` prefix before sending
- ❌ Don't send images > 5MB

### 2. User Experience
- ✅ Show loading state (5-10 sec wait time)
- ✅ Display jury votes individually for transparency
- ✅ Use demo mode for testing UI without AI calls
- ✅ Handle timeouts gracefully

### 3. Rate Limiting
- No hard limits currently
- Be respectful (this is a hackathon project)
- Each request costs $ in Bedrock API calls

---

## 🔗 CORS Configuration

The API has CORS enabled for all origins:

```python
allow_origins=["*"]
allow_methods=["*"]
allow_headers=["*"]
```

You can call it from any domain/localhost without issues.

---

## 📞 Support

**Issues?** Check:
1. Backend is running: `curl http://YOUR_EC2_IP:8000/api/health`
2. Request format matches examples above
3. Image is properly base64 encoded (no data URI prefix)
4. Timeout set to at least 30 seconds

**Expected Response Times:**
- Demo mode: Instant
- Real mode: 5-10 seconds

---

## 🎯 Quick Reference

**Base URL:** `http://YOUR_EC2_IP:8000`

**Key Endpoints:**
- `GET /api/health` - Health check
- `POST /api/judge` - Main endpoint (JSON)
- `POST /api/judge/upload` - File upload endpoint
- `POST /api/demo` - Demo mode (always wins)

**Request:**
```json
{
  "plea": "string (required, min 3 chars)",
  "image_base64": "string (optional, base64 JPEG)",
  "demo_mode": false
}
```

**Response:**
```json
{
  "verdict": "GRANTED|DENIED",
  "reasoning": "string",
  "roast": "string",
  "jury_votes": {
    "skeptic": "REAL|FAKE",
    "doctor": "CRITICAL|STABLE",
    "gambler": "IN|OUT"
  }
}
```

---

**Built for AWS re:Invent Hackathon** 🚽🎰

