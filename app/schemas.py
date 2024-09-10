
from typing import Union, Optional
from pydantic import BaseModel, Field
from datetime import datetime


# category stuff

class CategoryBase(BaseModel):
    id: int
    name: str

class CategoryCreate(BaseModel):
    name: str

class CategoryUpdate(BaseModel):
    name: str
    # updatedAt: datetime

class Category(CategoryBase):
    id: int
    createdAt: datetime
    updatedAt: datetime

    class Config:
        from_attributes = True


# product stuff

class ProductBase(BaseModel):
    id: int
    name: str
    price: int
    description: str
    imageUrl: Union[str, None] = None
    categoryId: int

class ProductCreate(BaseModel):
    name: str
    price: int
    description: str
    imageUrl: Union[str, None] = None
    categoryId: int

class Product(ProductBase):
    id: int
    createdAt: datetime
    updatedAt: datetime

    class Config:
        from_attributes = True

class ProductUpdate(BaseModel):
    name: str
    price: int
    description: str
    imageUrl: Union[str, None] = None
    categoryId: int



# Review stuff

class ReviewBase(BaseModel):
    id: int
    userImgUrl: Union[str, None]
    author: str
    content: Union[str, None] = Field(None, max_length=200, description="max 200 characters!")
    stars: int = Field(..., ge=1, le=5, description="The quantity must be between 1 and 5")
    productId: int

class ReviewCreate(BaseModel):
    # author: str
    content: Union[str, None] = Field(None, max_length=200, description="max 200 characters!")
    stars: int = Field(..., ge=1, le=5, description="The quantity must be between 1 and 5")

class Review(ReviewBase):
    id: int
    userId: int
    createdAt: datetime
    updatedAt: datetime


    class Config:
        from_attributes = True

class ReviewUpdate(BaseModel):
    content: Union[str, None] = Field(None, max_length=200, description="max 200 characters!")
    stars: int = Field(..., ge=1, le=5, description="The quantity must be between 1 and 5")
    # updatedAt: datetime



# User Stuff

class UserBase(BaseModel):
    id: int
    firstname: str
    lastname: Union[str, None] = None
    email: str
    imageUrl: Union[str, None] = None
    is_Admin: Union[bool, None] = None

class UserCreate(BaseModel):
    firstname: str
    lastname: Union[str, None] = None
    email: str
    password: str
    imageUrl: Union[str, None] = None

class User(UserBase):
    reviews: list[Review] = []
    createdAt: datetime
    updatedAt: datetime

    class Config:
        from_attributes = True


# Login stuff

class UserCredentials(BaseModel):
    email: str
    password: str


# Token Response

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenPayload(BaseModel):
    exp: int
    sub: Union[str, int]


class Healthz(BaseModel):
    status: str