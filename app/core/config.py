"""
App configuration. To pass values put them to .env file or directly env
"""
import string
from typing import Any, Optional, List, Union
from urllib.parse import quote

from passlib.context import CryptContext
from pydantic import EmailStr, PostgresDsn, field_validator, AnyHttpUrl
from pydantic_core.core_schema import FieldValidationInfo
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Project constants
    """
    DEBUG: bool = True
    API_V1_STR: str = "/api/v1"

    # security
    SECRET_KEY: str
    TOKEN_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 3
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 7 * 360  # 7 days
    REFRESH_TOKEN_LENGTH_BYTES: int = 32
    VERIFICATION_CODE_ALPHABET: str = string.ascii_uppercase + string.digits
    VERIFICATION_CODE_LEN: int = 6
    PASSWD_CONTEXT: CryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto")

    # SERVER_NAME: str
    DOMAIN: str
    SERVER_HOST: AnyHttpUrl

    # testing and development CORS
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost", "http://localhost:8080",
                                       "http://localhost:8000", "http://127.0.0.1",
                                       "http://127.0.0.1:8080", "http://127.0.0.1:8000",
                                       "https://localhost", "https://localhost:8080",
                                       "https://localhost:8000", "https://127.0.0.1",
                                       "https://127.0.0.1:8080", "https://127.0.0.1:8000",
                                       "https://temp.ortieom.ru", "https://truston.mzr.su"]

    # production CORS TODO: update when FQDN is determined
    # BACKEND_CORS_ORIGINS: List[str] = ["https://FQDN"]

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        """
        Validates and assembles CORS origins
        """
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        if isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @field_validator("SQLALCHEMY_DATABASE_URI", mode="before")
    @classmethod
    def assemble_db_connection(cls, val: Optional[str], info: FieldValidationInfo) -> Any:
        """
        Validates and assembles database URI
        """
        values = info.data

        if isinstance(val, str):
            return val

        path = f"{values.get('POSTGRES_USER')}:" \
               f"{quote(values.get('POSTGRES_PASSWORD'))}@" \
               f"{values.get('POSTGRES_SERVER')}/{values.get('POSTGRES_DB') or ''}" \
               f"?ssl=require"
        return "postgresql+asyncpg://" + path

    SMTP_PORT: Optional[int] = 465
    SMTP_HOST: Optional[str] = 'smtp.gmail.com'
    EMAILS_FROM_EMAIL: Optional[EmailStr] = None
    SMTP_PASSWORD: Optional[str] = None

    USER_BOT_TOKEN: str

    IMAGE_STORAGE_LOCATION: str = "./images/"
    IMAGE_SERVING_LOCATION: str = 'images'

    COOKIE_SETTINGS: Optional[dict] = None

    @field_validator("COOKIE_SETTINGS", mode="before")
    @classmethod
    def define_cookie_params(cls, val: Optional[dict], info: FieldValidationInfo):
        """
        Updates default cookie settings for debug
        """
        values = info.data

        if isinstance(val, dict):
            return val

        cookie_settings = {"httponly": True,
                           "samesite": 'strict',
                           "secure": True,
                           "domain": values.get('DOMAIN')}
        return cookie_settings

    TONCENTER_API_KEY: str

    class Config:
        """
        These settings parameters
        """
        case_sensitive = True
        env_file = '.env'


settings = Settings()
