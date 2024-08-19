from fastapi import HTTPException, status
import json
import bcrypt

from sqlalchemy.orm import Session
from .schemas import EmailAuthRequest, NewUserRequest, NewUserResponse, EmailVerification, LoginRequest, LogoutResponse
from .models import User

from core.config import settings
from core.redis_config import redis_config

from .utils import send_email_verif_link, generate_random_code, get_email_verif_complete_template, generate_jwt, decode_authorization_token, decode_token

rd = redis_config()

# Login
def login(db: Session, login_req: LoginRequest):
    # Select user from db
    user = db.query(User).filter(User.email == login_req.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email does not exist."
        )

    # Validate password
    if not bcrypt.checkpw((login_req.password).encode('utf-8'), (user.password).encode('utf-8')):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Password is wrong."
        )

    # Generate JWT
    return generate_jwt(user=user)


# Logout
def logout(db: Session, authorization: str):
    # Decode header
    token = decode_authorization_token(authorization=authorization)

    # Decode token
    user = decode_token(db=db, token=token)

    # Remove session
    rd.delete(f'{user.user_id}_refresh')

    return LogoutResponse(user_id=user.user_id)


# Remove account
def remove_account(db: Session, authorization: str):
    # Decode header
    token = decode_authorization_token(authorization=authorization)

    # Decode token
    user = decode_token(db=db, token=token)

    # Remove session
    rd.delete(f'{user.user_id}_refresh')

    # Remove user data

    # Remove user
    db.delete(user)
    db.commit()


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
def validate_nickname(db: Session, nickname: str):
    # Nickname length validation
    if len(nickname) > 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nickname is too long."
        )

    user = db.query(User).filter(User.nickname == nickname).first()
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nickname already exists."
        )


# Check email verification
def check_email_verification(email_req: str):
    # Check Redis
    rd_json = rd.get(email_req)
    rd_data = json.loads(rd_json)
    if not rd_json or not rd_data.get('verified'):
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
    user = db.query(User).filter(User.nickname == new_user.nickname).first()
    if user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nickname validation required."
        )

    # Encrypt password
    salt = bcrypt.gensalt()
    password_enc = bcrypt.hashpw((new_user.password).encode('utf-8'), salt)

    # Add user to db
    db_user = User(email=new_user.email,
                   password=password_enc,
                   nickname=new_user.nickname,
                   user_phone=new_user.phone,
                   user_address=new_user.address)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    print(f"New user {db_user.user_id} created.")

    return NewUserResponse(user_id=db_user.user_id)
