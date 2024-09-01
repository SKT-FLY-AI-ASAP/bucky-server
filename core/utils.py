import jwt
from sqlalchemy.orm import Session
from starlette import status

from core.config import settings
from core.redis_config import redis_config
from core.exceptions import BaseCustomException

from src.user.models import User

jwt_secret = settings.JWT_SECRET


# Decode access token and get user
def decode_access_token(db: Session, authorization: str):
    token = decode_authorization_token(authorization=authorization)
    return decode_token(db=db, token=token)


# Decode authorization token
def decode_authorization_token(authorization: str):
    # Check if token exists
    if not authorization:
        raise BaseCustomException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token required."
        )

    # Check bearer
    if not authorization.startswith('Bearer '):
        raise BaseCustomException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token."
        )

    token = authorization[len('Bearer '):]
    return token


# Decode token
def decode_token(db: Session, token: str, is_access: bool = True):
    if is_access:
        token_type = 'access_token'
    else:
        token_type = 'refresh_token'

    # Read payload
    try:
        payload = jwt.decode(token, jwt_secret, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise BaseCustomException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired."
        )
    except jwt.InvalidTokenError:
        raise BaseCustomException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token."
        )

    # Check type
    if payload['type'] != token_type:
        raise BaseCustomException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token."
        )

    # Find user from DB
    user = db.query(User).filter(User.user_id == payload['user_id']).first()

    # Check payload and user
    if not user:
        raise BaseCustomException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization failed."
        )

    # Check Redis (Session)
    rd = redis_config()
    rd_refresh = rd.get(f'{user.user_id}_refresh')
    if not rd_refresh:
        raise BaseCustomException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Login required."
        )

    return user
