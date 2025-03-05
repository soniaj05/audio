# app/services/ai_chat.py
import google.generativeai as genai
from fastapi import HTTPException
import logging
from app.config import settings

logger = logging.getLogger(__name__)
genai.configure(api_key=settings.GEMINI_API_KEY)
gemini_model = genai.GenerativeModel("gemini-1.5-flash-latest")

def generate_answer(question: str, context: str) -> str:
    try:
        logger.info(f"Generating answer for question: {question}")
        logger.info(f"Context: {context}")
        prompt = f"Based on the following transcript from a video, answer the question:\n\nTranscript: {context}\n\nQuestion: {question}\n\nAnswer:"
        response = gemini_model.generate_content(prompt)
        return response.text
    except Exception as e:
        logger.error(f"Failed to generate answer using Gemini: {str(e)}")
        return "Sorry, I couldn't generate an answer at the moment. Please try again later."