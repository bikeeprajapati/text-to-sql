from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.chat import ChatRequest, ChatResponse, ClarificationQuestion
from app.schemas.common import QueryStatus
from app.database.schema_inspector import get_database_schema
from app.database.connection import get_db
from app.models.chat import ChatSession, ChatMessage
from app.services.clarification import check_clarification_needed
from app.services.sql_generator import generate_sql
from app.services.sql_validator import is_sql_safe
from app.services.query_executor import execute_sql
from app.services.auth_dependency import get_current_user
from app.models.user import User

router = APIRouter(prefix="/chat", tags=["chat"])


def _save_message(db: Session, session_id: int, role: str, message_type: str, content: str) -> None:
    message = ChatMessage(
        session_id=session_id,
        role=role,
        message_type=message_type,
        content=content
    )
    db.add(message)
    db.commit()


@router.post("", response_model=ChatResponse)
def send_message(payload: ChatRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Handle a new chat message."""
    schema = get_database_schema()

    # Reuse the session if session_id was sent and it belongs to this user, otherwise create a new one
    if payload.session_id is None:
        session = ChatSession(user_id=current_user.id)
        db.add(session)
        db.commit()
        db.refresh(session)
    else:
        try:
            session = db.get(ChatSession, int(payload.session_id))
        except ValueError:
            session = None
        if session is None or session.user_id != current_user.id:
            raise HTTPException(status_code=404, detail="Session not found")

    session_id = session.id

    _save_message(db, session_id, "user", "question", payload.message)

    # Build the conversation so far, so the AI sees earlier questions and answers
    conversation = "\n".join(
        f"{m.role}: {m.content}"
        for m in session.messages
        if m.message_type != "sql_result"
    )

    result = check_clarification_needed(conversation, schema)

    if result["needs_clarification"]:
        _save_message(db, session_id, "assistant", "clarification_question", result["question"])

        return ChatResponse(
            session_id=str(session_id),
            status=QueryStatus.CLARIFICATION_NEEDED,
            message="I need a bit more information.",
            clarification=ClarificationQuestion(question=result["question"])
        )

    generated_sql = generate_sql(conversation, schema)

    if generated_sql is None:
        error_message = "I couldn't generate a SQL query for that. Try rephrasing."
        _save_message(db, session_id, "assistant", "error", error_message)
        return ChatResponse(
            session_id=str(session_id),
            status=QueryStatus.FAILED,
            message=error_message,
            generated_sql=None
        )

    if not is_sql_safe(generated_sql):
        error_message = "The generated SQL is not safe to execute."
        _save_message(db, session_id, "assistant", "error", error_message)
        return ChatResponse(
            session_id=str(session_id),
            status=QueryStatus.FAILED,
            message=error_message,
            generated_sql=None
        )

    results = execute_sql(generated_sql)
    if results is None:
        error_message = "Failed to execute the generated SQL."
        _save_message(db, session_id, "assistant", "error", error_message)
        return ChatResponse(
            session_id=str(session_id),
            status=QueryStatus.FAILED,
            message=error_message,
            generated_sql=None
        )

    _save_message(db, session_id, "assistant", "sql_result", generated_sql)

    return ChatResponse(
        session_id=str(session_id),
        status=QueryStatus.EXECUTED,
        message="Here's the generated SQL.",
        generated_sql=generated_sql,
        result=results
    )