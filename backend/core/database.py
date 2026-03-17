from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from config import settings


class Database:
    def __init__(self, url: str):
        self.engine = create_async_engine(
            url=url,
        )
        self.sessionmaker = async_sessionmaker(
            self.engine,
            class_=AsyncSession,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    async def get_session(self) -> AsyncSession:
        async with self.sessionmaker() as session:
            yield session
            await session.close()


database = Database(url=settings.database)