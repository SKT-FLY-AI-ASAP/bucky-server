from fastapi import HTTPException, status

from passlib.context import CryptContext

from sqlalchemy.orm import Session
from .schemas import NewUserRequest, NewUserResponse
from .models import User

from core.redis_config import redis_config

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
rd = redis_config()

def add_user(db: Session, new_user: NewUserRequest):
    # # Email validation
    # if not rd.get(new_user.email):
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Email authentication required."
    #     )

    # # Nickname validation
    # if not rd.get(new_user.nickname):
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Nickname validation required."
    #     )

    # Add user to db
    db_user = User(email=new_user.email,
                   password=pwd_context.hash(new_user.password),
                   nickname=new_user.nickname,
                   user_phone=new_user.phone,
                   user_address=new_user.address)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    print(f"New user {db_user.user_id} created.")

    return db_user.user_id
