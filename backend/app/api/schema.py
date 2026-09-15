from fastapi import APIRouter
from app.schemas.schema import ConnectDatabaseRequest, DatabaseSchemaResponse, TableInfo, ColumnInfo
from app.database.schema_inspector import get_database_schema

router = APIRouter(prefix="/schema", tags=["schema"])


@router.post("/connect")
def connect_database(payload: ConnectDatabaseRequest):
    return {"status": "connected"}


@router.get("", response_model=DatabaseSchemaResponse)
def get_schema():
    raw_schema = get_database_schema()
    

    tables = []
    for table_name, raw_columns in raw_schema.items():
        columns = [ColumnInfo(**col) for col in raw_columns]
        table_info = TableInfo(name=table_name, columns=columns)

        tables.append(table_info)

    return DatabaseSchemaResponse(tables=tables)