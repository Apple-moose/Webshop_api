from datetime import datetime
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import ValidationError
from app import database, models
from app.schemas import TokenPayload, Token, UserBase
from app.auth import ALGORITHM, JWT_SECRET_KEY
from sqlalchemy.orm import Session

reuseable_oauth = OAuth2PasswordBearer(
    # (Also in main.py)
    # tokenUrl="/docslogin",  
    tokenUrl="/auth/login",
    scheme_name="JWT"
)

async def get_current_user(token: str = Depends(reuseable_oauth)) -> UserBase:
    
    try:
        db = database.SessionLocal()

        payload = jwt.decode(
            token, JWT_SECRET_KEY, algorithms=[ALGORITHM]
        )
        # print('payload is: ',payload)
       
        token_data = TokenPayload(**payload)
        # print('token_data is: ',token_data)

        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # Extracting a specific value from the payload
    # user_id: str = payload.get("sub")

    [user_id, email] = token_data.sub.split(":")
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not Authorized !!",
        )

    return user


def is_user_admin(db: Session, user_id: int ):
    admin = db.query(models.User).filter(
        models.User.id == user_id).filter(
        models.User.is_Admin == True
        ).first()
    return admin