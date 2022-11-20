from email.policy import HTTP
from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, utils, models, oauth2

router = APIRouter(
    tags = ["authentication"]
)

@router.post("/login", response_model=schemas.Token)
# async def login(user_credentials: schemas.UserLogin, db: Session = Depends(get_db)):
async def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):


    # OAuth2PasswordRequestForm - zwraca username oraz password (a nie email)
    # user = db.query(models.Users).filter(models.Users.email == user_credentials.email).first()
    user = db.query(models.Users).filter(models.Users.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Invalid credentials.")

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Invalid credentials.")
    
    access_token = oauth2.create_acces_token(data = {"user_id": user.id})


    return {"access_token": access_token, "token_type": "bearer"}