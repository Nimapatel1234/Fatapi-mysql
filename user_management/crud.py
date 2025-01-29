from sqlalchemy.orm import Session
from . import models, schemas
from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta
from .schemas import UserUpdate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(
        name=user.name,
        profilepic=user.profilepic,
        cellnumber=user.cellnumber,
        password=hashed_password,
        email=user.email,
        roleId=user.roleId if user.roleId else 2  # Default role for normal user
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def update_user(db: Session, user_id: int, user: schemas.UserUpdate):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        return None  # Handle case where user doesn't exist

    db_user.profilepic = user.profilepic
    db_user.name = user.name
    db_user.email = user.email
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    return False  # Handle case where user doesn't exist

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_access_token(db: Session, user_id: int):
    token = jwt.encode(
        {'sub': user_id, 'exp': datetime.utcnow() + timedelta(minutes=30)},
        'secret', algorithm='HS256'
    )
    access_token = models.AccessToken(token=token, ttl=30000, userId=user_id)
    db.add(access_token)
    db.commit()
    db.refresh(access_token)
    return access_token
