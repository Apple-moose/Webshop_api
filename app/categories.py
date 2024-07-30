from sqlalchemy.orm import Session
from . import models, schemas

# get categories

def get_categories(db: Session, skip: int = 0, limit: int = 20):
    categories = db.query(models.Category).offset(skip).limit(limit).all()
    print(categories)
    return categories

def get_category(db: Session, cat_id: int):
    category = db.query(models.Category).filter(
    models.Category.id == cat_id).first()
    return category

# Create Category

def create_category(db: Session, cat: schemas.CategoryCreate):
    db_cat = models.Category(**cat.dict())
    db.add(db_cat)
    db.commit()
    db.refresh(db_cat)
    return db_cat


def update_category(
        db: Session, 
        category: schemas.CategoryUpdate, 
        cat_id: int):
    db_cat = db.query(models.Category).filter(
    models.Category.id == cat_id).first()
    updated_fields = category.model_dump(exclude_unset=True)
    for key, value in updated_fields.items():
        setattr(db_cat, key, value)  
    db.commit()
    db.refresh(db_cat)
    return db_cat