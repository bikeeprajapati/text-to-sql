from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.history import HistoryResponse, HistoryItem
from app.schemas.common import QueryStatus
from app.database.connection import get_db
from app.models.chat import ChatSession
from app.services.auth_dependency import get_current_user
from app.models.user import User

router = APIRouter(prefix="/history", tags=["history"])


@router.get("", response_model=HistoryResponse)
def get_history(session_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        session = db.get(ChatSession, int(session_id))
    except ValueError:
        session = None
    if session is None or session.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Session not found")

    messages = session.messages

    items = []
    for i, message in enumerate(messages):
        if message.role != "user":
            continue

        next_message = messages[i + 1] if i + 1 < len(messages) else None

        if next_message is None:
            continue

        if next_message.message_type == "sql_result":
            status = QueryStatus.EXECUTED
            generated_sql = next_message.content
        elif next_message.message_type == "clarification_question":
            status = QueryStatus.CLARIFICATION_NEEDED
            generated_sql = None
        elif next_message.message_type == "error":
            status = QueryStatus.FAILED
            generated_sql = None
        else:
            continue

        items.append(HistoryItem(
            id=str(message.id),
            session_id=session_id,
            question=message.content,
            generated_sql=generated_sql,
            status=status,
            created_at=message.created_at
        ))

    return HistoryResponse(items=items, total=len(items))