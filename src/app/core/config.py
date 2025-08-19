from pydantic_settings import BaseSettings
from pathlib import Path

import os
from dotenv import load_dotenv

load_dotenv()


BASE_DIR = Path(__file__).parent.parent.parent
print(BASE_DIR)


class Settings(BaseSettings):
    db_url: str = os.getenv("DATABASE_URL")
    db_name: str = os.getenv("POSTGRES_DB")


settings = Settings()
