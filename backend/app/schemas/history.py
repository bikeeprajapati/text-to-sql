from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel
from app.schemas.common import QueryStatus


class HistoryItem(BaseModel):
    id: str
    session_id: str
    question: str
    generated_sql: Optional[str] = None
    status: QueryStatus
    created_at: datetime


class HistoryResponse(BaseModel):
    items: List[HistoryItem]
    total: int