# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.routes import user_routes, audio_routes, chat_routes
from app.database import Base, engine

# Initialize FastAPI app
app = FastAPI()

# Serve static files
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(user_routes.router)
app.include_router(audio_routes.router)
app.include_router(chat_routes.router)

# Initialize database
Base.metadata.create_all(bind=engine)