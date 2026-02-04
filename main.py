from dotenv import load_dotenv
load_dotenv()   # MUST be first
from fastapi import FastAPI, Depends
from auth import verify_api_key
from models import RequestPayload, AgentResponse
from memory import get_session
from detector import detect_scam
from extractor import extract
from agent import agent_reply
from callback import send_final_callback

app = FastAPI()

@app.post("/honeypot", response_model=AgentResponse)
def honeypot(payload: RequestPayload, auth=Depends(verify_api_key)):
    session = get_session(payload.sessionId)

    # Save message
    session["messages"].append(payload.message.dict())

    # Detect scam
    is_scam, keywords = detect_scam(payload.message.text)
    if is_scam:
        session["scamDetected"] = True
        session["intelligence"]["suspiciousKeywords"] += keywords

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
