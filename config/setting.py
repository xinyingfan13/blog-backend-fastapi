import os
import sys
from typing import List

from dotenv import load_dotenv

load_dotenv()


class BaseSettings:
    version: str = "v1"
    title: str = "Piano Retailing"
    docs_url: str = "/docs"
    openapi_url: str = "/openapi.json"
    root_prefix: str = ""
    api_router_prefix: str = f"/api/{version}"

    cors_origins: List[str] = ["*"]

    stage: str = os.getenv("ENVIRONMENT", "local")

    db_name: str = os.getenv("DB_NAME", "piano_retailing")
    db_port: int = os.getenv("DB_PORT", 5432)

    jwt_secret_key: str = os.getenv("JWT_SECRET_KEY", "")
    jwt_algorithm: str = "HS256"
    jwt_default_expire_minutes: int = 30 * 24 * 60

    email_port = os.getenv("EMAIL_PORT", 587)
    email_host = os.getenv("EMAIL_HOST", "smtp.sendgrid.net")
    email_host_user = os.getenv("EMAIL_HOST_USER", "apikey")
    email_host_pwd = os.getenv("EMAIL_HOST_PASSWORD", "")
    default_from_email = os.getenv("DEFAULT_FROM_EMAIL", "")


class DevSettings(BaseSettings):
    """
    Development config
    """
    cluster_arn: str = os.getenv("CLUSTER_ARN", "")
    secret_arn: str = os.getenv("SECRET_ARN", "")


class LocalSettings(BaseSettings):
    """
    Local config
    """
    db_host: str = os.getenv("DB_HOST", "localhost")
    db_user: str = os.getenv("DB_USER", "")
    db_password: str = os.getenv("DB_PASSWORD", "")


class TestSetting(BaseSettings):
    """
    Test config
    """
    ENVIRONMENT: str = "test"


def get_config_based_on_stage():
    """
    Get app configurations for different stages
    """
    if "pytest" in sys.modules:
        return TestSetting()

    stage = os.getenv("ENVIRONMENT", "local")

    if stage == "dev":
        return DevSettings()
    elif stage == "local":
        return LocalSettings()

    return LocalSettings()


settings = get_config_based_on_stage()



