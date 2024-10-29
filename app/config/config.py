from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Fugle Statistics"
    fugledata_base_url: str
    class Config:
        env_file = ".env"


settings = Settings()  # type: ignore