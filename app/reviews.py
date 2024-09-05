from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from . import models, schemas


# get review by id
def get_review(db: Session, user_id:int, rev_id: int):
    review = db.query(models.Review).filter(
    models.Review.id == rev_id).filter(
    models.Review.userId == user_id).first()
    return review


# get reviews by product_id
def get_reviews_by_product_id(db: Session, prod_id: int, skip: int = 0, limit: int = 20):
    reviews = db.query(models.Review).filter(
    models.Review.productId == prod_id).offset(skip).limit(limit).all()
    return reviews


# get reviews by with userId
def get_users_reviews(
        db: Session, 
        user_id: int, 
        skip: int = 0, limit: int = 20):
    reviews = db.query(models.Review).filter(
    models.Review.userId == user_id).offset(skip).limit(limit).all()
    return reviews


#Update my review by reviewId
def update_review(
        db: Session, 
        review: schemas.ReviewUpdate, 
        rev_id: int):
    db_rev = db.query(models.Review).filter(
    models.Review.id == rev_id).first()
    updated_fields = review.model_dump(exclude_unset=True)
    for key, value in updated_fields.items():
        setattr(db_rev, key, value)  
    db.commit()
    db.refresh(db_rev)
    return db_rev


# Write a Review as user (by productId)
def create_review(db: Session, 
    rev: schemas.ReviewCreate,
    user_id: int,
    prod_id: int,
    user_imgUrl: str,
    author: str,
    ):
    db_rev = models.Review(**rev.dict(), 
    userId=user_id, author=author, productId=prod_id, userImgUrl= user_imgUrl)
    db.add(db_rev)
    db.commit()
    db.refresh(db_rev)
    return db_rev


# Erase my review (by review Id)
def delete_review(db: Session, user_id: int, rev_id: int):
    rev_db = db.query(models.Review).filter(
    models.Review.id == rev_id,
    models.Review.userId == user_id
    ).first()
    if not rev_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found."
        )
    try:
       db.delete(rev_db)
       db.commit()
       return rev_db
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while deleting the review: {str(e)}"
        )