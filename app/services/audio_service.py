# app/services/video_service.py
import os
import whisper
from fastapi import HTTPException
import logging
from app.database import get_db
from app.models.audio import Audio

logger = logging.getLogger(__name__)
model = whisper.load_model("base")

def validate_audio_file(file_path: str):
    # Check if the file exists
    if not os.path.exists(file_path):
        raise HTTPException(status_code=400, detail="Audio file is missing.")
    
    # Check if the file is empty
    if os.path.getsize(file_path) == 0:
        raise HTTPException(status_code=400, detail="Audio file is empty.")
    
    # Check if the file format is supported
    if not file_path.endswith(('.wav', '.mp3')):
        raise HTTPException(status_code=400, detail="Unsupported audio file format. Please upload a .wav or .mp3 file.")

def transcribe_audio(audio_filename: str) -> str:
    try:
        if not os.path.exists(audio_filename) or os.path.getsize(audio_filename) == 0:
            logger.error("Audio file is empty or missing before transcription.")
            raise HTTPException(status_code=400, detail="Audio file is empty or missing before transcription.")
        
        logger.info(f"Transcribing file: {audio_filename}, Size: {os.path.getsize(audio_filename)} bytes")
        result = model.transcribe(audio_filename)
        logger.info(f"Transcription successful: {result['text']}")
        return result['text']
    except Exception as e:
        logger.error(f"Failed to transcribe audio: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to transcribe audio: {str(e)}")

def process_audio_file(audio_filename: str, user_id: int, task_id: int):
    validate_audio_file(audio_filename)
    db = next(get_db())
    try:
        transcribed_text = transcribe_audio(audio_filename)
        print(f"transcribed text:{transcribed_text}")
        db_video = db.query(Audio).filter(Audio.id == task_id).first()
        if not db_video:
            logger.error(f"Video with task_id {task_id} not found")
            return
        db_video.transcribed = transcribed_text
        db.commit()
        logger.info(f"Database commit successful for video ID: {db_video.id}")
        db.refresh(db_video)
        logger.info(f"Video processed and saved: {db_video.id}")
        logger.info(f"Transcription: {transcribed_text}")
        return db_video.id
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to process video: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to process video: {str(e)}")
    finally:
        db.close()
        # Clean up the temporary file
        if os.path.exists(audio_filename):
            os.remove(audio_filename)
            logger.info(f"Temporary file {audio_filename} removed.")