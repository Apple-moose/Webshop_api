from passlib.context import CryptContext
from sqlalchemy.orm import Session
from . import models, schemas, auth
from fastapi import HTTPException


password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)


#Create a user
def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_hashed_password(user.password)
    db_user = models.User(
    firstname=user.firstname, 
    lastname=user.lastname, 
    email=user.email,
    password=hashed_password,
    imageUrl=user.imageUrl
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# User login & Create acess_token
def login_user(db: Session, user: schemas.UserCredentials):
    db_user = db.query(models.User).filter(
        models.User.email == user.email).first()

    user_password_error = "Incorrect username or password"

    if db_user is None:
        raise HTTPException(status_code=404, detail=user_password_error)
    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail=user_password_error)
    return {
        "access_token": auth.create_access_token(f"{db_user.id}:{db_user.email}"),
        "token_type": "bearer"}


#GET my user profile
def get_user(db: Session, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    return user


#GET my user by id
def get_user_by_id(db: Session, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    return user


#Docs login
def docs_login_user(db: Session, user: schemas.UserCredentials):
    db_user = db.query(models.User).filter(
        models.User.email == user.username).first()

    user_password_error = "Incorrect username or password"

    if db_user is None:
        raise HTTPException(status_code=404, detail=user_password_error)
    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail=user_password_error)
    return {
        "access_token": auth.create_access_token(f"{db_user.id}:{db_user.email}"),
        "token_type": "bearer"}

