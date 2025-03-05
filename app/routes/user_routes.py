# app/routes/user_routes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import *

from app.utils.security import hash_password,verify_password
from app.auth import create_access_token
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/users/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.phone == user.phone).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    hashed_password = hash_password(user.password)
    db_user = User(name=user.name, phone=user.phone, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/login/")
def login(login_request: login, db: Session = Depends(get_db)):
    try:
        # Query the database to find the user
        user = db.query(User).filter(User.name == login_request.name).first()

        # If user not found, raise an HTTP 404 error
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Verify the password
        if not verify_password(login_request.password, user.password):
            raise HTTPException(status_code=401, detail="Invalid password")

        # Create a JWT token
        token_data = {"sub": str(user.id)}  # Store user_id in the token
        token = create_access_token(token_data)

        # Return the token
        return {"message": "Login successful", "token": token}
    except Exception as e:
        logger.error(f"Failed to login: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to login: {str(e)}")