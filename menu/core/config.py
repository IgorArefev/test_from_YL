from dotenv import find_dotenv
from pydantic_settings import BaseSettings


class EnvSettings(BaseSettings):
    """Класс для работы с файлом .env."""

    app_name: str = "Меню"
    description: str = "Ylab"
    db_name: str
    db_port: int
    db_host: str
    db_user: str
    db_pass: str


settings = EnvSettings(_env_file=find_dotenv(".env"))
