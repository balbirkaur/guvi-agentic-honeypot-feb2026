sessions = {}

def get_session(session_id):
    return sessions.setdefault(session_id, {
        "messages": [],
        "intelligence": {
            "bankAccounts": [],
            "upiIds": [],
            "phishingLinks": [],
            "phoneNumbers": [],
            "suspiciousKeywords": []
        },
        "scamDetected": False
    })
