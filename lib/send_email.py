import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Dict

from fastapi import HTTPException
from jinja2 import FileSystemLoader, Environment

from common.constant import EMAIL_TEMPLATE_PATH
from config.setting import settings


os.makedirs(EMAIL_TEMPLATE_PATH, exist_ok=True)
template_loader = FileSystemLoader(searchpath=EMAIL_TEMPLATE_PATH)
template_env = Environment(loader=template_loader)


def send_email(email: str, subject: str, template_name: str, data: Dict) -> bool:
    try:
        template = template_env.get_template(template_name)
        html_content = template.render(data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error rendering HTML template: {str(e)}")

    # Create message object instance
    msg = MIMEMultipart()
    msg['From'] = settings.default_from_email
    msg['To'] = email
    msg['Subject'] = subject

    msg.attach(MIMEText(html_content, 'html'))

    try:
        # Establish SMTP connection
        with smtplib.SMTP(settings.email_host, settings.email_port) as server:
            server.starttls()
            server.login(settings.email_host_user, settings.email_host_pwd)
            server.sendmail(msg['From'], msg['To'], msg.as_string())
            return True

    except Exception as e:
        print("Send email failed: ", str(e))
        return False
