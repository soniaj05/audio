from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, UploadFile, File
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.audio import Audio
from app.models.user import User
from app.services.audio_service import process_audio_file
from app.auth import get_current_user
from app.utils.logger import *
import os

router = APIRouter()

@router.post("/videos/")
def create_video(
    background_tasks: BackgroundTasks,
    audio_file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    logger.info("Received request to upload video")
    logger.info(f"File: {audio_file.filename}, Size: {audio_file.size} bytes")
    if not current_user:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user_id = current_user.id
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Save the uploaded file temporarily
    tmp_folder = "tmp"
    os.makedirs(tmp_folder, exist_ok=True)
    file_path = os.path.join(tmp_folder, audio_file.filename)
    
    with open(file_path, "wb") as buffer:
        buffer.write(audio_file.file.read())
    
    db_video = Audio(file_path=file_path, transcribed="", user_id=user_id)
    db.add(db_video)
    db.commit()
    
    background_tasks.add_task(process_audio_file, file_path, user_id, db_video.id)
    
    return {"task_id": db_video.id, "status": "processing", "file_path":file_path}