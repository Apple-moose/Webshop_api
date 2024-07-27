from .database import Base
from sqlalchemy import Boolean, Column, ForeignKey, Text, Integer, String, DateTime, func
from sqlalchemy.orm import relationship

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True) 
    price = Column(Integer, index=True)
    description = Column(Text)
    imageUrl = Column(String)
    categoryId = Column(Integer, ForeignKey(
    "categories.id"), nullable=False)
    createdAt = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    updatedAt = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=False)

    category = relationship("Category", back_populates="products")

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True) 
    createdAt = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    updatedAt = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=False)

    products = relationship("Product", back_populates="category")

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    author = Column(String, nullable=False) 
    content = Column(Text)
    stars = Column(Integer)
    userId = Column(Integer, ForeignKey(
    "users.id"), nullable=False, index=True)
    productId = Column(Integer, ForeignKey(
    "products.id"), nullable=False, index=True)
    createdAt = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    updatedAt = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=False)

    user = relationship("User", back_populates="reviews")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=True)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    imageUrl = Column(String, nullable=True)
    disabled = Column(Boolean, default=False)
    createdAt = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    updatedAt = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=False)


    reviews = relationship("Review", back_populates="user") 


class Admin(Base):
    __tablename__ = "administrators"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    adminname = Column(String, nullable=False)
    password = Column(String, nullable=False)
    disabled = Column(Boolean, default=False)
    createdAt = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    updatedAt = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=False)