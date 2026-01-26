from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from .core.config import get_settings

settings = get_settings()

# Use the same database URL
DATABASE_URL = settings.database_url

engine = create_async_engine(DATABASE_URL, echo=settings.debug)

AsyncSessionLocal = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

class Base(DeclarativeBase):
    pass

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
