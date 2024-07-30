
from typing import Union, Optional
from pydantic import BaseModel, Field
from datetime import datetime


# category stuff

class CategoryBase(BaseModel):
    id: int
    name: str

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: str
    updatedAt: datetime

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

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int
    # category: list[Category] = []
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
    author: str
    content: Union[str, None] = None
    stars: int = Field(..., ge=1, le=5, description="The quantity must be between 1 and 5")
    productId: int

class ReviewCreate(ReviewBase):
    pass

class Review(ReviewBase):
    id: int
    userId: int #user-owner number
    createdAt: datetime
    updatedAt: datetime


    class Config:
        from_attributes = True

class ReviewUpdate(BaseModel):
    content: Union[str, None] = None
    stars: int = Field(..., ge=1, le=5, description="The quantity must be between 1 and 5")
    updatedAt: datetime



# User Stuff

class UserBase(BaseModel):
    id: int
    firstname: str
    lastname: Union[str, None] = None
    email: str
    imageUrl: Union[str, None] = None

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

# class Admin(UserBase):
#     is_Admin: Boolean


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