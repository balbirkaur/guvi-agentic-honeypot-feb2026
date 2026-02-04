from dotenv import load_dotenv
load_dotenv()  # MUST be first

from fastapi import FastAPI, Depends, Body, HTTPException, Header
from typing import Optional, Dict, List
from pydantic import BaseModel
import os
import time
import requests

# ==============================
# App
# ==============================
app = FastAPI()

# ==============================
# Authentication
# ==============================
API_KEY = os.getenv("API_KEY")

def verify_api_key(x_api_key: str = Header(...)):
    if not API_KEY or x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

# ==============================
# Models
# ==============================
class Message(BaseModel):
    sender: str
    text: str
    timestamp: int

class RequestPayload(BaseModel):
    sessionId: str
    message: Message
    conversationHistory: Optional[List[Dict]] = []
    metadata: Optional[Dict] = {}

class AgentResponse(BaseModel):
    status: str
    reply: str

# ==============================
# In-Memory Session Store
# ==============================
SESSIONS: Dict[str, Dict] = {}

def get_session(session_id: str):
    if session_id not in SESSIONS:
        SESSIONS[session_id] = {
            "messages": [],
            "scamDetected": False,
            "intelligence": {
                "bankAccounts": [],
                "upiIds": [],
                "phishingLinks": [],
                "phoneNumbers": [],
                "suspiciousKeywords": []
            }
        }
    return SESSIONS[session_id]

# ==============================
# Scam Detection (Simple Logic)
# ==============================
SCAM_KEYWORDS = ["blocked", "verify", "urgent", "upi", "account", "suspend"]

def detect_scam(text: str):
    found = [k for k in SCAM_KEYWORDS if k in text.lower()]
    return len(found) > 0, found

# ==============================
# Intelligence Extraction
# ==============================
def extract(text: str, intelligence: Dict):
    if "@upi" in text.lower():
        intelligence["upiIds"].append(text.strip())

    if "http" in text.lower():
        intelligence["phishingLinks"].append(text.strip())

# ==============================
# Agent Reply Logic
# ==============================
def agent_reply(turn_count: int) -> str:
    prompts = [
        "Why is my account being suspended?",
        "Can you explain the issue in detail?",
        "What should I do to avoid this?",
        "Is there any other way to verify?",
        "Please guide me step by step."
    ]
    return prompts[min(turn_count, len(prompts) - 1)]

# ==============================
# GUVI Callback
# ==============================
def send_final_callback(session_id: str, session: Dict):
    payload = {
        "sessionId": session_id,
        "scamDetected": True,
        "totalMessagesExchanged": len(session["messages"]),
        "extractedIntelligence": session["intelligence"],
        "agentNotes": "Scammer used urgency and verification pressure tactics"
    }

    try:
        requests.post(
            "https://hackathon.guvi.in/api/updateHoneyPotFinalResult",
            json=payload,
            timeout=5
        )
    except Exception:
        pass

# ==============================
# Honeypot Endpoint
# ==============================
@app.post("/honeypot", response_model=AgentResponse)
def honeypot(
    payload: Optional[RequestPayload] = Body(None),
    auth=Depends(verify_api_key)
):
    # GUVI Tester compatibility (empty / minimal body)
    if payload is None or payload.message is None:
        return {
            "status": "success",
            "reply": "Hello, how can I help you?"
        }

    session = get_session(payload.sessionId)

    # Save message
    session["messages"].append(payload.message.dict())

    # Scam detection
    is_scam, keywords = detect_scam(payload.message.text)
    if is_scam:
        session["scamDetected"] = True
        session["intelligence"]["suspiciousKeywords"].extend(keywords)

    # Intelligence extraction
    extract(payload.message.text, session["intelligence"])

    # Agent response
    reply = agent_reply(len(session["messages"]))

    # End condition → callback
    if session["scamDetected"] and len(session["messages"]) >= 8:
        send_final_callback(payload.sessionId, session)

    return {
        "status": "success",
        "reply": reply
    }
