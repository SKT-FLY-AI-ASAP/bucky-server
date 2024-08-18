from fastapi import APIRouter, Depends
from starlette import status

from .service import add_user

from core.database import get_db
from sqlalchemy.orm import Session
from .schemas import EmailAuthRequest, NewUserRequest, NewUserResponse

# Router
router = APIRouter(
    prefix="/api/v1/user",
)

# Add new user
@router.post("", response_model=NewUserResponse, status_code=status.HTTP_201_CREATED)
def add_new_user(db: Session = Depends(get_db), new_user: NewUserRequest = None):
    res = add_user(db, new_user=new_user)

    return {"user_id": res}
