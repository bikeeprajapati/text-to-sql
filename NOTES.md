# Text-to-SQL with Clarification Engine — Project Notes

## What this app does
Takes a natural language question, checks if it's answerable given the
connected database's schema, asks a clarifying question if it's ambiguous,
then generates and runs SQL.

## Request flow
1. User sends a question -> POST /api/chat
2. App inspects the connected DB's schema (tables/columns)
3. Clarification check: is the question answerable as-is?
   - If ambiguous -> return a clarifying question, wait for user's reply
   - If clear -> continue
4. Generate SQL from the (clarified) question + schema
5. Validate the SQL (safe, references real tables/columns)
6. Execute the SQL against the DB
7. Return results to the user
8. Log the exchange to history

## File status

### Done and tested
- database/connection.py - SQLAlchemy engine, connects to Supabase Postgres
- database/schema_inspector.py - get_database_schema() introspects real tables/columns
- services/llm_service.py - ask_llm(prompt) wraps Groq API (model: openai/gpt-oss-20b)
- services/clarification.py - format_schema_for_prompt() + check_clarification_needed()
  - full clarification engine working end-to-end: formats schema -> builds prompt ->
    calls Groq -> parses JSON -> returns {needs_clarification, question}
- schemas/*.py - Pydantic request/response shapes for chat, schema, history
- api/schema.py - GET /api/schema returns real live schema data
- api/chat.py - POST /api/chat wired to the clarification engine, tested live via /docs
  (both clarification_needed and sql_generated branches confirmed working)
- api/history.py - stub only, returns empty list


### In progress
- services/clarification.py
  - format_schema_for_prompt(schema_dict) - turns schema dict into readable
    text for the LLM prompt (WORKING, but needs to be re-derived from
    scratch - was AI-assisted, not fully understood yet)
  - TODO: build the actual clarification prompt (schema + user question)
  - TODO: call ask_llm(), parse JSON response
    ({"needs_clarification": bool, "question": str|null})

### Not started
- services/sql_generator.py - build SQL from clarified question + schema
- services/sql_validator.py - check generated SQL is safe before running
- services/query_executor.py - actually run the SQL, return rows
- models/ - SQLAlchemy tables for the app's own storage (chat sessions, history)
- tests/ - nothing written yet

## Gotchas learned the hard way
- Run uvicorn and `python3 -m app.x.y` from backend/, not from inside subfolders
  (imports are absolute, resolved from the app/ package root)
- SQLAlchemy's get_columns() has no 'primary_key' key - use
  inspector.get_pk_constraint(table) separately
- Special characters in DB passwords (@, #, etc.) must be percent-encoded
  in the connection string, or avoided entirely
- Side-effecting code (DB calls, API clients) belongs inside functions,
  not at module level, so importing a file doesn't trigger network calls
