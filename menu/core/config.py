from dotenv import find_dotenv
from pydantic_settings import BaseSettings


class EnvSettings(BaseSettings):
    """Класс для работы с файлами .env."""

    db_user: str
    db_pass: str
    db_host: str
    db_port: int
    db_name: str

    app_name: str
    description: str

    postgres_db: str
    postgres_user: str
    postgres_password: str

    redis_server: str
    redis_port: int
    redis_db: int

    mode: str

    @property
    def db_url(self) -> str:
        """url для подключения к БД"""
        return (
            'postgresql+asyncpg://'
            f'{settings.db_user}:'
            f'{settings.db_pass}@'
            f'{settings.db_host}:'
            f'{settings.db_port}/'
            f'{settings.db_name}'
        )

    class Config:
        if not find_dotenv('local.env'):
            env_file = find_dotenv('dev.env')
        else:
            env_file = find_dotenv('local.env')


settings = EnvSettings()
