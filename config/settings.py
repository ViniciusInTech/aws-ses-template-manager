from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    aws_region: Optional[str] = None
    aws_access_key_id: Optional[str] = None
    aws_secret_access_key: Optional[str] = None
    email_template_resources_path: Optional[str] = None

    openai_api_key: Optional[str] = None
    openai_model: Optional[str] = None
    openai_max_tokens: Optional[int] = None
    openai_temperature: Optional[float] = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
