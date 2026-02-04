SCAM_KEYWORDS = [
    "blocked", "urgent", "verify", "suspend",
    "upi", "click", "immediately", "account"
]

def detect_scam(text: str):
    hits = [k for k in SCAM_KEYWORDS if k in text.lower()]
    return len(hits) > 0, hits
