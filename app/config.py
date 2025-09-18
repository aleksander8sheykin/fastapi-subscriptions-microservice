# app/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    DB_POOL_SIZE: int
    DB_MAX_OVERFLOW: int

    SERVER_HOST: str
    SERVER_PORT: int

    LOG_LEVEL: str

    class Config:
        env_file = None
        env_file_encoding = 'utf-8'

settings = Settings()

