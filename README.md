# Agentic Honey-Pot for Scam Detection & Intelligence Extraction

## 🕵️ 1. Introduction

An AI-powered agentic honeypot that detects scam intent, engages scammers in multi-turn conversations, extracts actionable intelligence, and reports results to GUVI for automated evaluation.

Online scams are becoming increasingly adaptive. Traditional detection systems often fail as scammers change tactics in real-time. This project implements an **Agentic Honey-Pot**—an AI-powered system that detects scam intent and autonomously engages scammers to extract intelligence without revealing it has detected the fraud.

## 🎯 2. Objective

Design and deploy an AI-driven system that:

- Detects scam or fraudulent messages.
- Activates an autonomous AI Agent that maintains context across multi-turn conversations using session-based memory.
- Maintains a believable human-like persona.
- Extracts scam-related intelligence (UPI IDs, links, account numbers).
- Reports final results via a mandatory callback API.

---

## 🧠 3. System Architecture

Scammer Message  
→ Scam Intent Detector  
→ Agentic AI Persona (Multi-Turn Engagement)  
→ Intelligence Extraction Engine  
→ GUVI Final Result Callback

## 🛠 4. API Specification

### Authentication

Include these headers in every request:
| Header | Value |
| :--- | :--- |
| `Content-Type` | `application/json` |
| `x-api-key` | `YOUR_SECRET_API_KEY` |

### Engagement Endpoint

**POST** https://guvi-agentic-honeypot-feb2026-production.up.railway.app/honeypot

#### Request Body

```json
{
  "sessionId": "wertyu-dfghj-ertyui",
  "message": {
    "sender": "scammer",
    "text": "Your bank account will be blocked today. Verify immediately.",
    "timestamp": 1770005528731
  },
  "conversationHistory": [],
  "metadata": {
    "channel": "SMS",
    "language": "English",
    "locale": "IN"
  }
}
```

#### Response Body

```json
{
  "status": "success",
  "reply": "Why is my account being suspended?"
}
```

---

## 🔗 5. Mandatory Final Result Callback

Once the AI Agent has completed the engagement or extracted sufficient data, you **must** send the final payload to the GUVI evaluation endpoint.

**Endpoint:** `POST https://hackathon.guvi.in/api/updateHoneyPotFinalResult`

#### Final Payload Structure:

```json
{
  "sessionId": "abc123-session-id",
  "scamDetected": true,
  "totalMessagesExchanged": 18,
  "extractedIntelligence": {
    "bankAccounts": ["XXXX-XXXX-XXXX"],
    "upiIds": ["scammer@upi"],
    "phishingLinks": ["http://malicious-link.example"],
    "phoneNumbers": ["+91XXXXXXXXXX"],
    "suspiciousKeywords": ["urgent", "verify now", "account blocked"]
  },
  "agentNotes": "Scammer used urgency tactics and payment redirection"
}
```

---

## ⚖️ 6. Rules & Constraints

- **Persona:** The agent must behave like a real human and avoid revealing it is an AI or that it has detected a scam.
- **No Harassment:** Maintain ethical standards; no illegal instructions or harassment.
- **Mandatory Callback:** Failure to hit the `updateHoneyPotFinalResult` endpoint will result in the solution not being evaluated.
- **Intelligence Quality:** Accuracy in extracting UPI IDs and malicious links is a primary scoring factor.

## 🧠 Callback Trigger Condition:

The final callback is sent only after scam intent is confirmed AND sufficient engagement has occurred to extract meaningful intelligence.

## 📈 7. Evaluation Criteria

1.  **Detection Accuracy:** Precision in identifying scam intent.
2.  **Engagement Quality:** Natural flow of conversation.
3.  **Intelligence Depth:** Volume and accuracy of extracted scam data.
4.  **API Reliability:** Uptime and response speed.
5.  **Stealth:** Intelligence must be extracted without revealing that scam detection has occurred.

---

## 🚀 8. Setup & Deployment

1.  **Clone the Repository**
2.  **Install Requirements:** `pip install -r requirements.txt`
3.  **Configure Environment:** Add your API keys and the GUVI endpoint URL to `.env`.
4.  **Deploy:** Ensure your API is publicly accessible for evaluation.
