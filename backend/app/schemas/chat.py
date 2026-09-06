from typing import List, Optional
from pydantic import BaseModel, Field
from app.schemas.common import QueryStatus

# Data models for the API
class ChatRequest(BaseModel):
    session_id: Optional[str] = None
    message: str = Field(..., min_length=1, description="User's natural language question")

# Data model for a clarification question
class ClarificationQuestion(BaseModel):
    question: str
    options: Optional[List[str]] = None

# Data model for the chat response
class ChatResponse(BaseModel):
    session_id: str
    status: QueryStatus
    message: str
    clarification: Optional[ClarificationQuestion] = None
    generated_sql: Optional[str] = None
    result: Optional[List[dict]] = None
