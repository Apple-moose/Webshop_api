from sqlalchemy.orm import Session
from . import models, schemas

# get reviews

def get_reviews_by_product_id(db: Session, prod_id: int, skip: int = 0, limit: int = 20):
    reviews = db.query(models.Review).filter(
    models.Review.productId == prod_id).offset(skip).limit(limit).all()
    return reviews


# get reviews by userId

def get_reviews_by_user_id(db: Session, user_id: int, skip: int = 0, limit: int = 20):
    product = db.query(models.Review).filter(
    models.Review.userId == user_id).offset(skip).limit(limit).all()
    return product