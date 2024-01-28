from uuid import uuid4

from sqlalchemy import UUID
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    declared_attr,
    mapped_column
)

from menu.core.config import settings

DB_URL = (
    "postgresql+asyncpg://"
    f"{settings.db_user}:"
    f"{settings.db_pass}@"
    f"{settings.db_host}:"
    f"{settings.db_port}/"
    f"{settings.db_name}"
)


class Base(DeclarativeBase):
    """Базовый класс моделей."""

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4
    )


engine = create_async_engine(DB_URL)

AsyncSessionLocal = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    bind=engine
)


async def get_async_session():
    async with AsyncSessionLocal() as async_session:
        yield async_session
