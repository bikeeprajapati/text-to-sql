from app.database.connection import Base, engine
from app.models.chat import ChatSession, ChatMessage

Base.metadata.create_all(bind=engine)