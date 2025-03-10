# app/models/video.py
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from pydantic import BaseModel

class Audio(Base):
    __tablename__ = 'audio'
    id = Column(Integer, primary_key=True, autoincrement=True)
    file_path = Column(String(255), nullable=False)  
    transcribed = Column(Text, nullable=False)
    status=Column(String(50),default="pending")
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship("User", back_populates="audios")
    
class Audiocreate(BaseModel):
    file_path:str
    question:str