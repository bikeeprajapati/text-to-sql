from typing import List, Optional
from pydantic import BaseModel

# Data models for the API
class ColumnInfo(BaseModel):
    name: str
    data_type: str
    nullable: bool
    is_primary_key: bool = False

# Data model for a table
class TableInfo(BaseModel):
    name: str
    columns: List[ColumnInfo]

# Data model for the database schema response
class DatabaseSchemaResponse(BaseModel):
    tables: List[TableInfo]

# Data model for the database connection request
class ConnectDatabaseRequest(BaseModel):
    connection_string: Optional[str] = None
    host: Optional[str] = None
    port: Optional[int] = None
    database: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
