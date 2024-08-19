from jinja2 import Environment, FileSystemLoader
from pathlib import Path
from fastapi.responses import HTMLResponse
from starlette import status
import jwt

import string
import random
import datetime

from core.config import settings
from core.redis_config import redis_config

from .models import User
from .schemas import TokenResponse

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Generate JWT
def generate_jwt(user: User):
    jwt_secret = settings.JWT_SECRET
    payload_access = {
        'user_id': user.user_id,
        'nickname': user.nickname,
        'type': 'access_token'
    }
    payload_refresh = {
        'user_id': user.user_id,
        'nickname': user.nickname,
        'type': 'refresh_token'
    }

    # Timezone
    kst = datetime.timezone(datetime.timedelta(hours=9))
    kst_now = datetime.datetime.now(kst)

    # Token expiration time
    payload_access['exp'] = kst_now + datetime.timedelta(hours=24)
    payload_refresh['exp'] = kst_now + datetime.timedelta(hours=24 * 7)

    # Generate token
    access_token = jwt.encode(payload_access, jwt_secret, algorithm='HS256')
    refresh_token = jwt.encode(payload_refresh, jwt_secret, algorithm='HS256')

    # Add refresh token to redis
    rd = redis_config()
    rd.set(f'{user.user_id}_refresh', refresh_token, ex=60 * 60 * 24 * 7)

    return TokenResponse(access_token=access_token, refresh_token=refresh_token, user_id=user.user_id)


# Generate random code
def generate_random_code(length=15):
    # 사용할 문자 집합 정의
    characters = string.ascii_letters + string.digits

    # 랜덤 코드 생성
    random_code = ''.join(random.choices(characters, k=length))

    return random_code


# Send email
def send_email_verif_link(recipient: str, verif_link: str):
    # Email server config
    smtp_server = settings.MAIL_SERVER
    smtp_port = settings.MAIL_PORT
    smtp_sender = settings.MAIL_FROM
    smtp_password = settings.MAIL_PASSWORD

    # Jinja2 setting
    template_dir = Path('templates')
    template_env = Environment(loader=FileSystemLoader(template_dir))

    # Load template
    template = template_env.get_template('email_verification.html')

    # Render template with data
    html_content = template.render(link=verif_link)

    # Configure email
    msg = MIMEMultipart('alternative')
    msg['subject'] = settings.MAIL_SUBJECT
    msg['From'] = smtp_sender
    msg['To'] = recipient

    # Set HTML content
    part = MIMEText(html_content, 'html')
    msg.attach(part)

    # Connect server and send mail
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()  # TLS Encryption
        server.login(smtp_sender, smtp_password)
        server.sendmail(smtp_sender, recipient, msg.as_string())


# Html template
def get_email_verif_complete_template():
    # Jinja2 setting
    template_dir = Path('templates')
    template_env = Environment(loader=FileSystemLoader(template_dir))

    # Load template
    template = template_env.get_template('verification_res.html')

    # Render template with data
    content = template.render()

    return HTMLResponse(content=content, status_code=status.HTTP_200_OK)
