from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # API
    api_key: str = "dev-api-key-12345"
    
    # Database
    database_url: str = "sqlite:///./data/organizations.db"
    
    # Application
    app_name: str = "Organization Directory API"
    debug: bool = True
    
    # CORS
    cors_origins: list[str] = ["*"]
    
    class Config:
        env_file = ".env"


settings = Settings()