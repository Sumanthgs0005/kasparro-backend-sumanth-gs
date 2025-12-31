from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from app.core.config import settings

class Base(DeclarativeBase):
    __abstract__ = True
    metadata = None

class Database:
    def __init__(self):
        self.engine = create_async_engine(
            settings.database_url,
            echo=settings.echo_db_queries,
            future=True
        )
        self.session_factory = async_sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False
        )

db = Database()

async def get_session() -> AsyncSession:
    async with db.session_factory() as session:
        yield session
