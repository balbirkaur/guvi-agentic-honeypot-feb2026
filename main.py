from dotenv import load_dotenv
load_dotenv()  # MUST be first

from fastapi import FastAPI, Depends, Body
from typing import Optional
from pydantic import BaseModel

from auth import verify_api_key
from models import RequestPayload, AgentResponse
from memory import get_session
from detector import detect_scam
from extractor import extract
from agent import agent_reply
from callback import send_final_callback

app = FastAPI()


# -------------------------------
# GUVI Tester Compatible Model
# -------------------------------
class HoneypotRequest(BaseModel):
    sessionId: Optional[str] = "test-session"
    message: Optional[dict] = None
    conversationHistory: Optional[list] = []
    metadata: Optional[dict] = {}


# -------------------------------
# Honeypot Endpoint
# -------------------------------
@app.post("/honeypot", response_model=AgentResponse)
def honeypot(
    payload: Optional[RequestPayload] = Body(None),
    auth=Depends(verify_api_key)
):
    #  GUVI Tester sends empty or minimal body
    if payload is None or payload.message is None:
        return {
            "status": "success",
            "reply": "Hello, how can I help you?"
        }

    # -------------------------------
    # REAL HONEYPOT LOGIC
    # -------------------------------
    session = get_session(payload.sessionId)

    # Save incoming message
    session["messages"].append(payload.message.dict())

    # Detect scam
    is_scam, keywords = detect_scam(payload.message.text)
    if is_scam:
        session["scamDetected"] = True
        session["intelligence"]["suspiciousKeywords"].extend(keywords)

    # Extract intelligence
    extract(payload.message.text, session["intelligence"])

    # Agent reply
    reply = agent_reply(len(session["messages"]))

    # End condition (example: after 8 messages)
    if session["scamDetected"] and len(session["messages"]) >= 8:
        send_final_callback(payload.sessionId, session)

    return {
        "status": "success",
        "reply": reply
    }
