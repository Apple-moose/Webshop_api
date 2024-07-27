from sqlalchemy.orm import Session
from . import models, schemas

# get categories

def get_categories(db: Session, skip: int = 0, limit: int = 20):
    categories = db.query(models.Category).offset(skip).limit(limit).all()
    print(categories)
    return categories

# Create Category

def create_category(db: Session, cat: schemas.CategoryCreate):
    db_cat = models.Category(**cat.dict())
    db.add(db_cat)
    db.commit()
    db.refresh(db_cat)
    return db_cat


# def create_category(db: Session, user_id: int, cat: schemas.CategoryCreate):
#     db_cat = models.Category(**cat.dict(), owner_id=user_id)
#     db.add(db_cat)
#     db.commit()
#     db.refresh(db_cat)
#     return db_cat