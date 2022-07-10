from typing import List

from fastapi import Depends, FastAPI, HTTPException, Body
from sqlalchemy.orm import Session

from . import utils, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependencies
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/create", response_model=schemas.Response)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = utils.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return schemas.Response(message=utils.create_user(db=db, user=user))


@app.get("/users/", response_model=List[schemas.User])
def get_all_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = utils.get_all_users(db, skip=skip, limit=limit)
    return users


@app.patch("/users/toggle", response_model=schemas.Response)
async def toggle_user(user_id: int = Body(embed=True), db: Session = Depends(get_db)):
    user: models.User = utils.get_user_by_id(db=db, author_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user_status = user.is_active
    return schemas.Response(message=utils.toggle_user(db=db,user_id=user_id, user_status=user_status))


@app.get("/users/{email}", response_model=schemas.User)
def get_user_by_email(email: str, db: Session = Depends(get_db)):
    db_user = utils.get_user_by_email(db, email=email)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/posts/create", response_model=schemas.Response)
def create_post(
    post: schemas.PostCreate, db: Session = Depends(get_db)
):
    if not utils.get_user_by_id(db=db, author_id=post.author_id):
        raise HTTPException(status_code=404, detail="Author not found")
    return schemas.Response(message=utils.create_post(db=db, post=post))


@app.patch("/posts/update/{post_id}", response_model=schemas.Response)
async def update_post(post_id: int, post: schemas.PostUpdate, db: Session = Depends(get_db)):
    if not utils.get_posts_by_id(db=db, post_id=post_id):
        raise HTTPException(status_code=404, detail="Post not found")
    return schemas.Response(message=utils.update_post(db=db,post_id=post_id, post=post))


@app.delete("/posts/delete/{post_id}", response_model=schemas.Response)
async def delete_post(post_id: int,  db: Session = Depends(get_db)):
    if not utils.get_posts_by_id(db=db, post_id=post_id):
        raise HTTPException(status_code=404, detail="Post not found")
    return schemas.Response(message=utils.delete_post(db=db,post_id=post_id))


@app.get("/posts/{author_id}", response_model=List[schemas.Post])
def get_posts_by_author(author_id: int, db: Session = Depends(get_db)):
    if not utils.get_user_by_id(db=db, author_id=author_id):
        raise HTTPException(status_code=404, detail="Author not found")
    posts = utils.get_posts_by_author(db, author_id=author_id)
    return posts


@app.get("/posts/", response_model=List[schemas.Post])
def get_all_posts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    posts = utils.get_all_posts(db, skip=skip, limit=limit)
    return posts



