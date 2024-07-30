import os
from datetime import datetime, timedelta
from typing import Union, Any
from jose import jwt

# configuration
ACCESS_TOKEN_EXPIRE_MINUTES = 90  #min
ALGORITHM = "HS256"
JWT_SECRET_KEY = os.environ['JWT_SECRET_KEY']


# create JWT
# beware utcnow is deprecated, can replace by :
# datetime.now(timezone.utc).replace(tzinfo=None)

def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
       expires_delta = datetime.utcnow() + expires_delta
    else:
       expires_delta = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
    return encoded_jwt