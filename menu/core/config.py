from dotenv import find_dotenv, load_dotenv
from pydantic_settings import BaseSettings

load_dotenv(find_dotenv(".env"))


class Settings(BaseSettings):
    app_name: str = "Меню"
    description: str = "Ylab"
    db_name: str
    db_port: str
    db_host: str
    db_user: str
    db_pass: str


settings = Settings()
