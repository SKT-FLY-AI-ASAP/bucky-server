from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse
from starlette import status

from .service import add_user, send_email, verify_link, validate_nickname, check_email_verification

from core.database import get_db
from sqlalchemy.orm import Session
from .schemas import EmailAuthRequest, NewUserRequest, NewUserResponse
from core.schemas import ResponseDto, DataResponseDto

# Router
router = APIRouter(
    prefix="/api/v1/user",
)


# Request email verification link
@router.post("/link", response_model=ResponseDto, status_code=status.HTTP_201_CREATED)
def send_email_auth_link(db: Session = Depends(get_db), email: EmailAuthRequest = None):
    send_email(db, email_req=email)

    return ResponseDto(message="Link sent.")


# Request email verification via link
@router.get("/link", response_class=HTMLResponse)
def verify_email_link(email: str = None, code: str = None):
    return verify_link(email, code)


# Check email verification
@router.get("/email", response_model=ResponseDto, status_code=status.HTTP_200_OK)
def check_email(email: str):
    check_email_verification(email_req=email)

    return ResponseDto(message="Verified.")


# Validate nickname
@router.get("/nickname", response_model=ResponseDto, status_code=status.HTTP_200_OK)
def check_nickname(db: Session = Depends(get_db), nickname: str = None):
    validate_nickname(db, nickname=nickname)

    return ResponseDto(message="OK.")


# Add new user
@router.post("", response_model=DataResponseDto[NewUserResponse], status_code=status.HTTP_201_CREATED)
def add_new_user(db: Session = Depends(get_db), new_user: NewUserRequest = None):
    res = add_user(db, new_user=new_user)

    return DataResponseDto(data=res, message="Created.")
