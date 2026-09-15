from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import chat, schema, history

app = FastAPI(
    title="Text-to-SQL API",
    description="Natural language to SQL with a clarification engine",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "text-to-sql-api"
    }

app.include_router(chat.router, prefix="/api", tags=["chat"])
app.include_router(schema.router, prefix="/api", tags=["schema"])
app.include_router(history.router, prefix="/api", tags=["history"])