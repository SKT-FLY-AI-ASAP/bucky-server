from jinja2 import Environment, FileSystemLoader
from pathlib import Path

from core.config import settings

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

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
