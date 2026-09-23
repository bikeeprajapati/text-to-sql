from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.connection import Base


class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id = Column(Integer, primary_key=True, index=True)

    created_at = Column(DateTime, default=datetime.utcnow)  

    messages = relationship("ChatMessage", back_populates="session", order_by="ChatMessage.id")


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)

    session_id = Column(Integer, ForeignKey("chat_sessions.id"))

    role = Column(String, nullable=False)

    message_type = Column(String, nullable=False)

    content = Column(Text, nullable=False)  

    created_at = Column(DateTime, default=datetime.utcnow)

    session = relationship("ChatSession", back_populates="messages")