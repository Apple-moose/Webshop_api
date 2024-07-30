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

#Update y review by reviewId
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