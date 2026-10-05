from app.database.connection import Base, engine
from app.models.chat import ChatSession, ChatMessage
from app.models.user import User

Base.metadata.drop_all(bind=engine, tables=[ChatMessage.__table__, ChatSession.__table__])
Base.metadata.create_all(bind=engine)