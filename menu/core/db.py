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

TEST_DB_URL = (
    "postgresql+asyncpg://"
    f"{settings.db_test_user}:"
    f"{settings.db_test_pass}@"
    f"{settings.db_test_host}:"
    f"{settings.db_test_port}/"
    f"{settings.db_test_name}"
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
test_engine = create_async_engine(TEST_DB_URL)

AsyncSessionLocal = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    bind=engine
)

TestAsyncSessionLocal = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    bind=test_engine
)


async def get_async_session():
    async with AsyncSessionLocal() as async_session:
        yield async_session


async def get_test_async_session():
    async with TestAsyncSessionLocal() as test_async_session:
        yield test_async_session
