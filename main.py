
from typing import List
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from app import categories, reviews, users, database, schemas, products, auth
# from app.deps import get_current_user


load_dotenv()

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()



# sign up users

@app.post("/auth/signup", response_model=schemas.UserBase)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return users.create_user(db, user=user)

# Login

# @app.post("/auth/login", response_model=schemas.Token)
# def login_user(user: schemas.UserCredentials, db: Session = Depends(get_db)):
#     return users.login_user(db, user=user)


# This dependency will make sure get_current_user below will
# always receive the `token` as a string.
reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/docslogin",  # only for usage in the docs!
    scheme_name="JWT"
)

# @app.post("/docslogin", response_model=schemas.Token)
# def login_with_form_data(
#     user: OAuth2PasswordRequestForm = Depends(),
#     db: Session = Depends(get_db)
# ):
#     return users.login_user(db, user=user)


# get user's profile

# @app.get("/auth/me", response_model=schemas.UserBase)
# def get_user(user: schemas.UserBase = Depends(get_current_user)):
#     return user
@app.get("/auth/{id}", response_model=schemas.User)
def user_by_id(
    id: int,
    db: Session = Depends(get_db)):
    results = users.get_user_by_id(db, user_id=id)
    if results is None:
        raise HTTPException(status_code=404, detail="No user found!!")
    return results


# get products list

@app.get("/products", response_model=List[schemas.Product])
def read_products(
    skip: int = 0, limit: int = 20,
    # user: schemas.UserBase = Depends(get_current_user),
    db: Session = Depends(get_db)):
    # results = lists.get_lists(db, user_id=user.id, skip=skip, limit=limit)
    results = products.get_products(db, skip=skip, limit=limit)
    if results is None:
        raise HTTPException(status_code=404, detail="No lists found")
    return results

# Get Product by Id

@app.get("/products/{prod_id}", response_model=schemas.Product)
def read_product(
    prod_id: int,
    db: Session = Depends(get_db)):
    results = products.get_product_by_id(db, prod_id=prod_id)

    if results is None:
        raise HTTPException(status_code=404, detail="No lists found")
    return results


#GET Products by category's name

@app.get("/products/category/name:{category_name}", response_model=List[schemas.Product])
def get_products_list_by_category_name(
    category_name: str,
    db: Session = Depends(get_db)):
    categoryId = products.find_product_id_from_name(db, cat_name=category_name)
    results = products.get_products_list_by_category_id(db, cat_id=categoryId)
    if results is None:
        raise HTTPException(status_code=404, detail="No lists found")
    return results


#GET Products by category's Id

@app.get("/products/category/categoryId:{category_id}", response_model=List[schemas.Product])
def products_list_by_categoryId(
    category_id: int,
    db: Session = Depends(get_db)):
    results = products.get_products_list_by_category_id(db, cat_id=category_id)
    if results is None:
        raise HTTPException(status_code=404, detail="No lists found")
    return results



# Get Categories list

@app.get("/categories", response_model=List[schemas.Category])
def read_categories(
    skip: int = 0, limit: int = 20,
    # user: schemas.UserBase = Depends(get_current_user),
    db: Session = Depends(get_db)):
    # results = lists.get_lists(db, user_id=user.id, skip=skip, limit=limit)
    results = categories.get_categories(db, skip=skip, limit=limit)
    if results is None:
        raise HTTPException(status_code=404, detail="No lists found")
    return results


# create category

@app.post("/categories", response_model=schemas.Category)
def create_category(
    category: schemas.CategoryCreate, 
    # user: schemas.UserBase = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # return categories.create_category(db, user_id=user.id, list=list)
    return categories.create_category(db, cat=category)


# Get reviews by productId
@app.get("/reviews/productId:{prod_id}", response_model=List[schemas.Review])
def get_reviews_by_product_id(
    prod_id: int,
    skip: int = 0, limit: int = 20,
    db: Session = Depends(get_db),

):
    results = reviews.get_reviews_by_product_id(db, prod_id=prod_id, skip=skip, limit=limit)
    if results is None:
        raise HTTPException(status_code=404, detail="No lists found")
    return results


# get reviews by userId

@app.get("/reviews/userId:{user_id}", response_model=List[schemas.Review])
def get_reviews_by_product_id(
    user_id: int,
    skip: int = 0, limit: int = 20,
    db: Session = Depends(get_db),

):
    results = reviews.get_reviews_by_user_id(db, user_id=user_id, skip=skip, limit=limit)
    if results is None:
        raise HTTPException(status_code=404, detail="No lists found")
    return results

# Get List per id


# @app.get("/lists/{list_id}", response_model=schemas.List)
# def read_list(
#     list_id: int,
#     user: schemas.UserBase = Depends(get_current_user),
#     db: Session = Depends(get_db)):
#     results = lists.get_list(db, list_id=list_id, user_id=user.id)
#     if results is None:
#         raise HTTPException(status_code=404, detail="No lists found")
#     return results

# create list


# @app.post("/lists", response_model=schemas.List)
# def create_list(
#     list: schemas.ListCreate, 
#     user: schemas.UserBase = Depends(get_current_user),
#     db: Session = Depends(get_db)
# ):
#     return lists.create_list(db, user_id=user.id, list=list)

# delete list


# @app.delete("/lists/{list_id}", response_model=schemas.List)
# def delete_lists(
#     list_id: int, 
#     user: schemas.UserBase = Depends(get_current_user),
#     db: Session = Depends(get_db)):
#     return lists.delete_list(db, user_id=user.id, list_id=list_id)

#GET Task with lists id and auth

# @app.get("/lists/{list_id}/tasks", response_model=List[schemas.Task])
# def read_tasks(
#     list_id: int,
#     user: schemas.UserBase = Depends(get_current_user),
#     skip: int = 0, 
#     limit: int = 20, 
#     db: Session = Depends(get_db)):
#     results = tasks.get_tasks(db, list_id=list_id, user_id=user.id, skip=skip, limit=limit)
#     if results is None:
#         raise HTTPException(status_code=404, detail="No lists found")
#     return results



# get task with its items


# @app.get("/tasks", response_model=List[schemas.Task])
# def read_tasks(
#     skip: int = 0, 
#     limit: int = 20, db: Session = Depends(get_db)):
#     results = tasks.get_tasks(db, skip=skip, limit=limit)
#     if results is None:
#         raise HTTPException(status_code=404, detail="No lists found")
#     return results


#GET Task with lists id and auth

# @app.get("/lists/{list_id}/tasks/{id}", response_model=schemas.Task)
# def read_tasks(
#     list_id: int,
#     id: int,
#     user: schemas.UserBase = Depends(get_current_user),
#     db: Session = Depends(get_db)):
#     results = tasks.get_task_by_list_id(db, list_id=list_id, user_id=user.id, task_id=id)
#     if results is None:
#         raise HTTPException(status_code=404, detail="No lists found")
#     return results


# create task


# @app.post("/tasks", response_model=schemas.Task)
# def create_task(list: schemas.Task, db: Session = Depends(get_db)):
#     return tasks.create_task(db, list=list)


# create task with list_id and auth


# @app.post("/lists/{list_id}/tasks", response_model=schemas.Task)
# def create_list_task(
#     list_id: int,
#     task: schemas.TaskCreate,
#     user: schemas.UserBase = Depends(get_current_user),
#     db: Session = Depends(get_db)
# ):
#   	# FIRST, try to fetch the list for this user
#     list = lists.get_list(db, user_id=user.id, list_id=list_id)

#     # 404 if the list isn't accessible / not found
#     if list is None:
#         raise HTTPException(status_code=404, detail="List not found")
#     else:
#       	# SECOND, proceed with creation of the task, only if the list is accessible for this user.
#         return tasks.create_task_id(db, list_id=list_id, task=task)
    


# delete task


# @app.delete("/tasks", response_model=schemas.Task)
# def delete_tasks(list_id: int, db: Session = Depends(get_db)):
#     return tasks.delete_task(db, list_id=list_id)


# DELETE specific tasks with list_id (auth)

# @app.delete("/lists/{list_id}/tasks/{id}", response_model=schemas.Task)
# def delete_tasks_by_id(
#     list_id: int,
#     id: int,
#     user: schemas.UserBase = Depends(get_current_user),
#     db: Session = Depends(get_db)):
#     return tasks.delete_task_by_id(
#         db,
#         list_id=list_id,
#         task_id=id,
#         user_id=user.id,
#     )

#UPDATE a specific Task with auth

# @app.put("/lists/{list_id}/tasks/{id}", response_model=schemas.TaskUpdate)
# async def update_task(
#     list_id: int,
#     id: int,
#     updated_data: schemas.TaskUpdate, 
#     user: schemas.UserBase = Depends(get_current_user), 
#     db: Session = Depends(get_db)):

#     check_list = lists.get_list(db, list_id=list_id, user_id=user.id)

#     if check_list is None:
#         raise HTTPException(status_code=404, detail="List not found")
#     else:
#         return tasks.update_task_by_id(
#         db, 
#         list_id=list_id,
#         task_id=id, 
#         updated_data=updated_data)


# @app.get("/healthz", response_model=schemas.Healthz)
# def healthz():
#     return {"status": "ok"}


