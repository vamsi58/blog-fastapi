from sqlalchemy.orm import Session

from . import models, schemas


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_id(db: Session, author_id: int):
    return db.query(models.User).filter(models.User.id == author_id).first()


def get_all_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(
        email=user.email,
        hashed_password=fake_hashed_password,
        first_name=user.first_name,
        last_name=user.last_name,
        mobile=user.mobile,
        registered_at=user.registered_at,
        intro=user.intro,
        profile=user.profile
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return "User created successfully"


def toggle_user(db: Session, user_id: int, user_status: bool):
    db.query(models.User).filter(models.User.id == user_id).update(dict([("is_active", not user_status)]))
    db.commit()
    return f"User status changed to {'Enabled' if not user_status else 'Disabled'}"


def get_all_posts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Post).offset(skip).limit(limit).all()


def get_posts_by_author(db: Session, author_id: int):
    return db.query(models.Post).filter(models.Post.author_id == author_id).all()


def get_posts_by_id(db: Session, post_id: int):
    return db.query(models.Post).filter(models.Post.id == post_id).all()


def create_post(db: Session, post: schemas.PostCreate):
    db_post = models.Post(**post.dict())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return "Post created successfully"


def update_post(db: Session, post_id:int, post: schemas.PostUpdate):
    db.query(models.Post).filter(models.Post.id == post_id).update(post.dict())
    db.commit()
    return "Post updated successfully"


def delete_post(db: Session, post_id:int):
    db.query(models.Post).filter(models.Post.id == post_id).delete()
    db.commit()
    return "Post deleted successfully"



