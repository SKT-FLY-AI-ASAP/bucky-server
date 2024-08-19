from fastapi import HTTPException, status
import json

from passlib.context import CryptContext

from sqlalchemy.orm import Session
from .schemas import EmailAuthRequest, NewUserRequest, NewUserResponse, EmailVerification, NicknameValidRequest
from .models import User

from core.config import settings
from core.redis_config import redis_config

from .utils import send_email_verif_link, generate_random_code, get_email_verif_complete_template

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
rd = redis_config()


# Send email link
def send_email(db: Session, email_req: EmailAuthRequest):
    # Check if email exists
    user = db.query(User).filter(User.email == email_req.email).first()
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists."
        )

    # Generate verification link
    code = generate_random_code()
    link = f"{settings.BASE_URL}:{settings.PORT}/api/v1/user/link?email={email_req.email}&code={code}"

    # Send mail
    try:
        send_email_verif_link(recipient=email_req.email, verif_link=link)
        print(f"Mail sent successfully. - {email_req.email}")
    except Exception as e:
        print(str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to send email. - {email_req.email}"
        )

    # Add to redis
    data = EmailVerification(code=code, verified=False).model_dump()
    rd.set(email_req.email, json.dumps(data))
    print(f"Redis data saved successfully. - {data}")


# Verify email link
def verify_link(email: str, code: str):
    # Check redis
    rd_json = rd.get(email)
    if not rd_json:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email does not exist."
        )

    rd_data = json.loads(rd_json)
    if rd_data.get('code') != code:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid link."
        )
    elif rd_data.get('verified'):
        return get_email_verif_complete_template()

    # Add to redis
    data = EmailVerification(code=code, verified=True).model_dump()
    rd.set(email, json.dumps(data))
    print(f"Redis data saved successfully. - {data}")

    # HTML Response
    return get_email_verif_complete_template()


# Validate nickname
def validate_nickname(db: Session, nickname_req: NicknameValidRequest):
    # Nickname validation
    user = db.query(User).filter(User.nickname == nickname_req.nickname)
    if user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nickname validation required."
        )


# Check email verification
def check_email_verification(email_req: EmailAuthRequest):
    # Check Redis
    rd_json = rd.get(email_req.email)
    if not rd_json:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email verification required."
        )


# Add new user
def add_user(db: Session, new_user: NewUserRequest):
    # Email validation
    if not rd.get(new_user.email):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email verification required."
        )

    # Nickname validation
    user = db.query(User).filter(User.nickname == new_user.nickname)
    if user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nickname validation required."
        )

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

    return NewUserResponse(user_id=db_user.user_id)
