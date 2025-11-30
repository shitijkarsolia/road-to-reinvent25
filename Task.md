



If you build a standard "Yelp for Toilets," you will lose because it is practical, helpful, and boring. The judges want "Delightfully Impractical."

To win, we need to take this idea and make it hostile, over-engineered, and absurd.

Here is the winning pivot:

🚽 The Pivot: "Hold It." (The Gatekeeping Bathroom App)



The Concept:
A crowdsourced bathroom finder that refuses to show you the location unless you can prove to an AI Jury that you are desperate enough to use it.
It gamifies the biological struggle. If you aren't suffering, you don't get the door code.



The "Delightfully Impractical" Twist:
Instead of just showing a map, the user must undergo a "Desperation Verification" process.

Step 1: The user requests a bathroom.

Step 2: The App (AI) says: "I don't believe you. Upload a selfie showing your 'O-Face' (Urgency Face)."

Step 3: AWS Rekognition analyzes the face.

If "Calm": ACCESS DENIED. "You can hold it. Try again in 10 minutes."

If "Distressed": ACCESS GRANTED. The map unlocks.

🛠️ The 5-Hour Bus Build Plan

Hour 1: The Map (Frontend)

Goal: A blurred-out map (Google Maps/Mapbox) with locked icons.

Kiro Prompt: "Build a React Map component where all markers are locked. When clicked, open a modal that says 'VERIFICATION REQUIRED'."

Hour 2: The Judge (AWS Rekognition)

Goal: Analyze the selfie.

Tech: AWS Lambda receives the image 
→
→
 Calls AWS Rekognition (DetectFaces).

Logic: Look for specific attributes: EyesOpen: false, MouthOpen: true, Emotion: Fear/Disgust.

Kiro Prompt: "Write a Lambda function that returns 'Authorized' only if the Rekognition confidence score for 'Distressed' is above 90%."

Hour 3: The Interrogator (Bedrock)

Goal: If the face check is borderline, make the user "Beg" via text.

Tech: AWS Bedrock (Claude 3 Haiku).

Persona: A snobby nightclub bouncer. "Look, this is a VIP Restroom. Why should I let you in? Describe your pain."

Hour 4: The Crowdsourcing (The "Review" System)

Goal: Make the reviews useless.

Twist: Users don't rate cleanliness. They rate "Acoustics" and "WiFi Latency."

Kiro Prompt: "Generate a review form that asks for 'Reverb Delay' and 'Tile Texture' instead of star ratings."

Hour 5: The Demo Polish

The Visuals: Add a "Bladder Meter" that fills up red on the screen.

The Sound: A ticking clock sound that gets faster the longer the AI interrogates you.

🎤 The 60-Second Demo Script

The Hook (10s): "We built a bathroom finder. But we realized that in Vegas, bathrooms are for closers. Introducing Hold It: The app that gatekeeps toilets."

The Fail (20s):

Teammate: "I really need to go!" (Smiles at camera).

App: ACCESS DENIED. "AWS Rekognition detects a smile. You are clearly fine."

The Success (20s):

Teammate: (Makes a horrific, grimacing face at the webcam).

App: ANALYZING... DESPERATION LEVEL: CRITICAL.

App: "Access Granted. Proceed to the nearest Portapotty immediately."

The Close (10s): "Hold It. Because you shouldn't pee unless you earn it."

Why this wins:
It takes a "boring" idea (bathroom finder) and adds Computer Vision (Rekognition) and GenAI (Bedrock) in a way that is technically impressive but hilariously unnecessary.