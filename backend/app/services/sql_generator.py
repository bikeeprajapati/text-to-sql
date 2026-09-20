import json
from app.services.llm_service import ask_llm
from app.services.clarification import format_schema_for_prompt


SQL_GENERATION_PROMPT_TEMPLATE = """You are a text-to-SQL assistant. Given a database schema and a user's question, write a single read-only SQL query (SELECT only - never INSERT, UPDATE, DELETE, or DROP) that answers it.

Database schema:
{schema}

User's question: "{question}"

Respond with ONLY valid JSON, no other text, in exactly this format:
{{"sql": "SELECT ... ;"}}
"""


def generate_sql(user_question: str, schema_dict: dict) -> str:
    """
    Generates a SQL query for a (clarified, unambiguous) user question.
    Returns the SQL string, or None if generation/parsing fails.
    """
    schema_text = format_schema_for_prompt(schema_dict)

    prompt = SQL_GENERATION_PROMPT_TEMPLATE.format(schema=schema_text, question=user_question)

    raw_response = ask_llm(prompt)

    try:
        result = json.loads(raw_response)
        return result["sql"]
    except (json.JSONDecodeError, KeyError):
        return None


if __name__ == "__main__":
    from app.database.schema_inspector import get_database_schema

    schema = get_database_schema()
    sql = generate_sql("show me all customers in Kathmandu", schema)
    print(sql)