# app/models/chat.py
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import LONGTEXT 
from app.database import Base
from pydantic import BaseModel

class ChatHistory(Base):
    __tablename__ = 'chathistory'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    file_path = Column(String(255), nullable=False)
    question = Column(String(255), nullable=False)
    answer = Column(String(255), nullable=False)
    transcribed = Column(LONGTEXT, nullable=False)
    user = relationship("User", back_populates="chathistories")
    
class ChatHistoryCreate(BaseModel):
    user_id: int
    
class question(BaseModel):
    file_path:str
    question: str