import os
from collections.abc import AsyncGenerator

from sqlalchemy.engine import URL, make_url
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

async_engine: AsyncEngine | None = None
async_session_factory: async_sessionmaker[AsyncSession] | None = None

SYNC_TO_ASYNC_DRIVERS = {
    "postgresql": "postgresql+asyncpg",
    "postgres": "postgresql+asyncpg",
    "postgresql+psycopg2": "postgresql+asyncpg",
}


def get_database_url() -> URL:
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        raise RuntimeError("DATABASE_URL is not set")
    return make_url(database_url)


def get_async_database_url() -> str:
    url = get_database_url()
    async_driver = SYNC_TO_ASYNC_DRIVERS.get(url.drivername)
    if async_driver:
        url = url.set(drivername=async_driver)
    if url.drivername != "postgresql+asyncpg":
        raise RuntimeError(
            "DATABASE_URL must use PostgreSQL with asyncpg-compatible driver"
        )
    url = normalize_asyncpg_ssl(url)
    return url.render_as_string(hide_password=False)


def normalize_asyncpg_ssl(url: URL) -> URL:
    query = dict(url.query)
    sslmode = query.pop("sslmode", None)
    if sslmode and "ssl" not in query:
        query["ssl"] = "true" if sslmode != "disable" else "false"
    return url.set(query=query)


def get_int_env(name: str, default: int) -> int:
    raw_value = os.environ.get(name)
    if raw_value is None:
        return default
    try:
        value = int(raw_value)
    except ValueError as exc:
        raise RuntimeError(f"{name} must be an integer") from exc
    if value < 0:
        raise RuntimeError(f"{name} must be greater than or equal to 0")
    return value


def get_async_engine() -> AsyncEngine:
    global async_engine
    if async_engine is None:
        async_engine = create_async_engine(
            get_async_database_url(),
            pool_size=get_int_env("DATABASE_POOL_SIZE", 5),
            max_overflow=get_int_env("DATABASE_MAX_OVERFLOW", 5),
            pool_pre_ping=True,
        )
    return async_engine


def get_async_session_factory() -> async_sessionmaker[AsyncSession]:
    global async_session_factory
    if async_session_factory is None:
        async_session_factory = async_sessionmaker(
            get_async_engine(),
            expire_on_commit=False,
        )
    return async_session_factory


async def dispose_async_engine() -> None:
    global async_engine, async_session_factory
    if async_engine is not None:
        await async_engine.dispose()
    async_engine = None
    async_session_factory = None


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with get_async_session_factory()() as session:
        yield session
