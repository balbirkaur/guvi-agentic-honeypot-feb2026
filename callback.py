import requests

GUVI_URL = "https://hackathon.guvi.in/api/updateHoneyPotFinalResult"

def send_final_callback(session_id, session_data):
    payload = {
        "sessionId": session_id,
        "scamDetected": True,
        "totalMessagesExchanged": len(session_data["messages"]),
        "extractedIntelligence": session_data["intelligence"],
        "agentNotes": "Used urgency and payment redirection tactics"
    }

    requests.post(GUVI_URL, json=payload, timeout=5)
