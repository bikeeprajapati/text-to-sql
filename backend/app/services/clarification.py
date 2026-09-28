import json
from app.services.llm_service import ask_llm


def format_schema_for_prompt(schema_dict):
    """
    Format a schema dictionary into a string suitable for prompting the LLM.
    """
    formatted_schema = []
    for table_name, columns in schema_dict.items():
        formatted_columns = [
            f'{column["name"]} ({column["data_type"]}{", primary key" if column["is_primary_key"] else ""})'
            for column in columns
        ]
        formatted_schema.append(f"Table: {table_name}\nColumns: {', '.join(formatted_columns)}")
    return "\n\n".join(formatted_schema)


CLARIFICATION_PROMPT_TEMPLATE = """You are a text-to-SQL assistant. Given a database schema and a conversation with a user, decide if what the user wants is clear enough to write SQL for.

Database schema:
{schema}

Conversation so far (the user's later messages may answer clarifying questions asked earlier):
{question}

If the request is ambiguous (unclear metric, unclear time range, could match multiple tables, etc.), respond with a clarifying question.
If the request is clear enough to answer, say so.
If the user has already answered your earlier clarifying question, do not ask it again.

Respond with ONLY valid JSON, no other text, in exactly this format:
{{"needs_clarification": true, "question": "your clarifying question here"}}
or
{{"needs_clarification": false, "question": null}}
"""


def check_clarification_needed(user_question: str, schema_dict: dict) -> dict:
    """
    Checks if a user's question is ambiguous given the database schema.
    Returns a dict: {"needs_clarification": bool, "question": str or None}
    """
    schema_text = format_schema_for_prompt(schema_dict)

    prompt = CLARIFICATION_PROMPT_TEMPLATE.format(schema=schema_text, question=user_question)

    raw_response = ask_llm(prompt)

    try:
        result = json.loads(raw_response)
        return result
    except json.JSONDecodeError:
        return {"needs_clarification": False, "question": None}


if __name__ == "__main__":
    from app.database.schema_inspector import get_database_schema

    schema = get_database_schema()
    result = check_clarification_needed("show me all customers in Kathmandu", schema)
    print(result)