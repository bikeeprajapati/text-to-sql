from fastapi import APIRouter
from app.schemas.chat import ChatRequest, ChatResponse, ClarificationQuestion
from app.schemas.common import QueryStatus
from app.database.schema_inspector import get_database_schema
from app.services.clarification import check_clarification_needed
from app.services.sql_generator import generate_sql
from app.services.sql_validator import is_sql_safe
from app.services.query_executor import execute_sql
router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
def send_message(payload: ChatRequest):
    """Handle a new chat message."""
    schema = get_database_schema()

    result = check_clarification_needed(payload.message, schema)

    if result["needs_clarification"]:
        return ChatResponse(
            session_id=payload.session_id or "stub_session",
            status=QueryStatus.CLARIFICATION_NEEDED,
            message="I need a bit more information.",
            clarification=ClarificationQuestion(question=result["question"])
        )

    generated_sql = generate_sql(payload.message, schema)

    if not is_sql_safe(generated_sql):
        return ChatResponse(
            session_id=payload.session_id or "stub_session",
            status=QueryStatus.FAILED,
            message="The generated SQL is not safe to execute.",
            generated_sql=None
        )
    # Execute the generated SQL and return the results
    results = execute_sql(generated_sql)
    if results is None:
        return ChatResponse(
            session_id=payload.session_id or "stub_session",
            status=QueryStatus.FAILED,
            message="Failed to execute the generated SQL.",
            generated_sql=None
        )
    
    return ChatResponse(
    session_id=payload.session_id or "stub_session",
    status=QueryStatus.EXECUTED,
    message="Here's the generated SQL.",
    generated_sql=generated_sql,
    result=results
)