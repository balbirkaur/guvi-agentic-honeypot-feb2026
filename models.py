from pydantic import BaseModel
from typing import List, Optional

class Message(BaseModel):
    sender: str
    text: str
    timestamp: int

class RequestPayload(BaseModel):
    sessionId: str
    message: Message
    conversationHistory: List[Message] = []
    metadata: Optional[dict] = None

class AgentResponse(BaseModel):
    status: str
    reply: str
