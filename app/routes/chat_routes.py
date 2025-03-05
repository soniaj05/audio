# app/routes/chat_routes.py
from fastapi import APIRouter, Depends, HTTPException,File,UploadFile,Form
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.chat import *
from app.services.ai_chat import generate_answer
from app.models.audio import *
import time
from app.auth import get_current_user
from app.models.user import *
router = APIRouter()

@router.post("/ask/")

def ask_question(request: question, db: Session = Depends(get_db),current_user: User = Depends(get_current_user),):
    print("Ask endpoint hit!")
    if not current_user:
        raise HTTPException(status_code=401, detail="Invalid token") 
    audio = db.query(Audio).filter(Audio.file_path == request.file_path).first()
    if not audio:
        raise HTTPException(status_code=404, detail="Video not found")
    
    retries = 0
    while not audio.transcribed and retries < 10:
        time.sleep(1) 
        db.refresh(audio)  
        retries += 1
        
    if not audio.transcribed:
            return {"question": request.question, "answer": "Video transcription is not yet completed. Please try again later."}
    answer = generate_answer(request.question, audio.transcribed)
    chat_entry = ChatHistory(
        user_id=current_user.id,
        file_path=audio.file_path,
        question=request.question,
        answer=answer,
        transcribed=audio.transcribed
    )
    db.add(chat_entry)
    db.commit()
    db.refresh(chat_entry)
    return {"question": request.question, "answer": answer}

