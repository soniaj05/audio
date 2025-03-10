from openai import OpenAI
from fastapi import HTTPException
import logging
from app.config import settings

logger = logging.getLogger(__name__)
client = OpenAI(api_key=settings.OPENAI_API_KEY,  base_url="https://api.anthropic.com/v1/")  # Initialize the OpenAI client

def generate_answer(question: str, context: str) -> str:
    try:
        logger.info(f"Generating answer for question: {question}")
        logger.info(f"Context: {context}")
        
        prompt = f"Based on the following transcript from a video, answer the question:\n\nTranscript: {context}\n\nQuestion: {question}\n\nAnswer:"
        
        response = client.chat.completions.create(
            model="claude-3-7-sonnet-20250219",  # Use the chat-based model
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        
        return response.choices[0].message.content.strip()  # Access the response content
    except Exception as e:
        logger.error(f"Failed to generate answer using OpenAI: {str(e)}")
        return "Sorry, I couldn't generate an answer at the moment. Please try again later."