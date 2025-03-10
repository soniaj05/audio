# app/models/user.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base
from pydantic import BaseModel,field_validator

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    phone = Column(String(10), nullable=False)
    password = Column(String(255), nullable=False)
    audios = relationship("Audio", back_populates="user")
    chathistories = relationship("ChatHistory", back_populates="user")
    
class UserCreate(BaseModel):
    name: str
    phone: str
    password:str
    @field_validator('phone')
    @classmethod
    def validate_phone(cls, phone):
        if not phone.isdigit() or len(phone) != 10:
            raise ValueError("Phone number must be exactly 10 digits")
        return phone
    
class login(BaseModel):
    name:str
    password:str