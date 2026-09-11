from fastapi import APIRouter
from app.schemas.schema import ConnectDatabaseRequest, DatabaseSchemaResponse

router = APIRouter(prefix="/schema", tags=["schema"])


@router.post("/connect")
def connect_database(payload: ConnectDatabaseRequest):
    return {"status": "connected"}


@router.get("", response_model=DatabaseSchemaResponse)
def get_schema():
    return DatabaseSchemaResponse(tables=[])