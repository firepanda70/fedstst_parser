from enum import Enum

from pathlib import Path

from pydantic_settings import BaseSettings
import dotenv


dotenv.load_dotenv('.env')


class Config(BaseSettings):
    db_name: str
    db_host: str
    db_port: int
    db_user: str
    db_pass: str


config = Config()
