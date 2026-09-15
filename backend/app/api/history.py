from fastapi import APIRouter
from app.schemas.history import HistoryResponse

router = APIRouter(prefix="/history", tags=["history"])


@router.get("", response_model=HistoryResponse)
def get_history(session_id: str):
    return HistoryResponse(items=[], total=0)
    