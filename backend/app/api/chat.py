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

    # Save the incoming user message
    user_message = ChatMessage(
        session_id=session_id,
        role="user",
        message_type="question",
        content=payload.message
    )
    db.add(user_message)
    db.commit()
    conversation = "\n".join(
        f"{m.role}: {m.content}"
        for m in session.messages
        if m.message_type != "sql_result"
    )

    result = check_clarification_needed(conversation, schema)

    if result["needs_clarification"]:
        clarification_message = ChatMessage(
            session_id=session_id,
            role="assistant",
            message_type="clarification_question",
            content=result["question"]
        )
        db.add(clarification_message)
        db.commit()

        return ChatResponse(
            session_id=str(session_id),
            status=QueryStatus.CLARIFICATION_NEEDED,
            message="I need a bit more information.",
            clarification=ClarificationQuestion(question=result["question"])
        )

    generated_sql = generate_sql(conversation, schema)

    if not is_sql_safe(generated_sql):
        return ChatResponse(
            session_id=str(session_id),
            status=QueryStatus.FAILED,
            message="The generated SQL is not safe to execute.",
            generated_sql=None
        )
    results = execute_sql(generated_sql)
    if results is None:
        return ChatResponse(
            session_id=str(session_id),
            status=QueryStatus.FAILED,
            message="Failed to execute the generated SQL.",
            generated_sql=None
        )

    result_message = ChatMessage(
        session_id=session_id,
        role="assistant",
        message_type="sql_result",
        content=generated_sql
    )
    db.add(result_message)
    db.commit()

    return ChatResponse(
        session_id=str(session_id),
        status=QueryStatus.EXECUTED,
        message="Here's the generated SQL.",
        generated_sql=generated_sql,
        result=results
    )