from pydantic_settings import BaseSettings
from typing import Optional
from pathlib import Path

class Settings(BaseSettings):
    BASE_URL: Optional[str] = None
    PORT: Optional[int] = None
    DB_URL: Optional[str] = None
    DB_USER: Optional[str] = None
    DB_PASSWORD: Optional[str] = None

    class Config:
        env_file = Path(__file__).parent / '.env'
        env_file_encoding = 'utf-8'

settings = Settings()
