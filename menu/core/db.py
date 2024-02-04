from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from menu.core.config import settings

engine = create_async_engine(settings.db_url)

AsyncSessionLocal = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    bind=engine
)


async def get_async_session():
    async with AsyncSessionLocal() as async_session:
        yield async_session
