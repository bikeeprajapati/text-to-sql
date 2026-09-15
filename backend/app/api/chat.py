from fastapi import APIRouter
from app.schemas.chat import ChatRequest, ChatResponse
from app.schemas.common import QueryStatus

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
def send_message(payload: ChatRequest):
    return ChatResponse(
        session_id=payload.session_id or "stub_session",
        status=QueryStatus.CLARIFICATION_NEEDED,
        message="Stub response - service logic not yet wired in."
    )   

