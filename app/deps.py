# app/deps.py

from datetime import datetime
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import ValidationError
from app import database, models
from app.schemas import TokenPayload, Token, UserBase
from app.auth import ALGORITHM, JWT_SECRET_KEY

# This dependency will make sure get_current_user below will
# always receive the `token` as a string.
reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/docslogin",  # only for usage in the docs!
    scheme_name="JWT"
)
# Here, we receive the `token` as a string from `reusable_auth`
async def get_current_user(token: str = Depends(reuseable_oauth)) -> UserBase:
    
    try:
        db = database.SessionLocal()

        # the injected token here comes from the Authorization header
        # and is always present if we reach this code
        payload = jwt.decode(
            token, JWT_SECRET_KEY, algorithms=[ALGORITHM]
        )
        # print('payload is: ',payload)
       
        # Creating a TokenPayload instance using the payload dictionary
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

    # convert the string "id:username" in the token to [id, username]
    [user_id, username] = token_data.sub.split(":")
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not Authorized",
        )

    return user