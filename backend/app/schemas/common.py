from enum import Enum


class QueryStatus(str, Enum):
    CLARIFICATION_NEEDED = "clarification_needed"
    SQL_GENERATED = "sql_generated"
    EXECUTED = "executed"
    FAILED = "failed"
