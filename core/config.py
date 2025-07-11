from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """애플리케이션 설정"""
    
    # 마인크래프트 서버 설정
    minecraft_host: str = "localhost"
    minecraft_port: int = 25575
    minecraft_password: str
    
    # API 설정
    api_title: str = "Minecraft API"
    api_version: str = "1.0.0"

    # Telegram Bot Setting
    telegram_bot_token: str = ""
    telegram_chat_id: str = ""
    
    # 환경 변수 파일
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()