import os
from logging.config import fileConfig

from sqlalchemy import create_engine, pool
from sqlalchemy.engine import URL, make_url

from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = None

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

ASYNC_TO_SYNC_DRIVERS = {
    "postgresql+asyncpg": "postgresql+psycopg2",
    "postgres+asyncpg": "postgresql+psycopg2",
    "postgresql": "postgresql+psycopg2",
    "postgres": "postgresql+psycopg2",
}


def get_database_url() -> URL:
    database_url = os.environ.get("DATABASE_URL") or config.get_main_option(
        "sqlalchemy.url"
    )
    if not database_url:
        raise RuntimeError("DATABASE_URL is not set and sqlalchemy.url is empty")

    return make_url(database_url)


def get_sync_database_url() -> str:
    url = get_database_url()
    sync_driver = ASYNC_TO_SYNC_DRIVERS.get(url.drivername)
    if sync_driver:
        url = url.set(drivername=sync_driver)
    return url.render_as_string(hide_password=False)


def escape_config_value(value: str) -> str:
    return value.replace("%", "%%")


config.set_main_option("sqlalchemy.url", escape_config_value(get_sync_database_url()))


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


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = get_sync_database_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = create_engine(
        get_sync_database_url(),
        poolclass=pool.QueuePool,
        pool_size=get_int_env("DATABASE_POOL_SIZE", 5),
        max_overflow=get_int_env("DATABASE_MAX_OVERFLOW", 5),
        pool_pre_ping=True,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
