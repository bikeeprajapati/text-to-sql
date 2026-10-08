from sqlalchemy import Column, Integer, String, DateTime
from app.database.connection import Base
from app.utils.time import utc_now


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=utc_now)