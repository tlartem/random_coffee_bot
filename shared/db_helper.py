from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.model import Base


class DatabaseHelper:
    def __init__(
        self,
        url: str,
        echo: bool = False,
        echo_pool: bool = False,
        pool_size: int = 5,
        max_overflow: int = 10,
    ) -> None:
        if "sqlite" in url:
            self.engine: AsyncEngine = create_async_engine(
                url=url,
                echo=echo,
                echo_pool=echo_pool,
            )
        else:
            self.engine: AsyncEngine = create_async_engine(
                url=url,
                echo=echo,
                echo_pool=echo_pool,
                pool_size=pool_size,
                max_overflow=max_overflow,
            )

        self.session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    async def create_tables(self) -> None:
        async with self.engine.begin() as conn:
            # Используем run_sync для выполнения синхронных операций внутри асинхронного контекста
            await conn.run_sync(Base.metadata.create_all)

    async def dispose(self) -> None:
        await self.engine.dispose()

    @asynccontextmanager
    async def session_getter(self) -> AsyncGenerator[AsyncSession]:
        async with self.session_factory() as session:
            yield session

    async def get_session(self) -> AsyncGenerator[AsyncSession]:
        async with self.session_factory() as session:
            yield session
