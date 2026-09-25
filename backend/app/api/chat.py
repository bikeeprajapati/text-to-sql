from fastapi import APIRouter, Depends
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

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
def send_message(payload: ChatRequest, db: Session = Depends(get_db)):
    """Handle a new chat message."""
    schema = get_database_schema()

    # Get or create the session (always creates new, for now)
    new_session = ChatSession()
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    session_id = new_session.id

    # Save the incoming user message
    user_message = ChatMessage(
        session_id=session_id,
        role="user",
        message_type="question",
        content=payload.message
    )
    db.add(user_message)
    db.commit()

    result = check_clarification_needed(payload.message, schema)

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

    generated_sql = generate_sql(payload.message, schema)

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