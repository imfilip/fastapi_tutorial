from email.policy import HTTP
from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, utils, models

router = APIRouter(
    tags = ["authentication"]
)

@router.post("/login")
async def login(user_credentials: schemas.UserLogin, db: Session = Depends(get_db)):

    user = db.query(models.Users).filter(models.Users.email == user_credentials.email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid credentials.")

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid credentials.")
    
    return {"token": "example token 123"}