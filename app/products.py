from sqlalchemy.orm import Session
from sqlalchemy import func
from . import models, schemas


# get products
def get_products(db: Session, skip: int = 0, limit: int = 20):
    products = db.query(models.Product).offset(skip).limit(limit).all()
    return products


# get one product by id
def get_product_by_id(db: Session, prod_id: int):
    product = db.query(models.Product).filter(
    models.Product.id == prod_id).first()
    return product


# get products by category's name (func.lower for iLike sql function!!)
def find_product_id_from_name(db: Session, cat_name: str) -> int:
    category = db.query(models.Category).filter(
    func.lower(models.Category.name) == func.lower(cat_name)).first()
    
    if category is None:
        raise ValueError(f"No category found with name {cat_name}")
    
    cat_id = category.id
    return cat_id


# get products by categoryId
def get_products_list_by_category_id(
    db: Session, 
    cat_id: int,
    skip: int = 0,
    limit: int = 20
    ):
    products = db.query(models.Product).filter(
    models.Product.categoryId == cat_id
    ).offset(skip).limit(limit).all()
    return products


#create product
def create_product(db: Session, product: schemas.Product):
    db_pro = models.Product(**product.dict())
    db.add(db_pro)
    db.commit()
    db.refresh(db_pro)
    return db_pro


#Update Product
def update_product(
        db: Session, 
        product: schemas.ProductUpdate, 
        pro_id: int):
    db_pro= db.query(models.Product).filter(
    models.Product.id == pro_id).first()
    updated_fields = product.model_dump(exclude_unset=True)
    for key, value in updated_fields.items():
        setattr(db_pro, key, value)  
    db.commit()
    db.refresh(db_pro)
    return db_pro

#delete product
def delete_product(db: Session, pro_id: int):
    prod = db.query(models.Product).filter(
    models.Product.id == pro_id).first()
    db.delete(prod)
    db.commit()
    return prod

