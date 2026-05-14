import os
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.__version__ import APP_VERSION
from app.common.config.app_config import FastApiAppConfig
from app.common.db import dispose_async_engine
from app.dependencies.init_dependencies import init_dependencies
from app.routers.system_router import system_router
from app.routers.territory_router import territory_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_dependencies()
    yield
    await dispose_async_engine()


app_config = FastApiAppConfig(
    version=os.environ.get("APP_VERSION", APP_VERSION),
    name=os.environ.get("APP_NAME", "Example FastAPI App"),
    description=os.environ.get("APP_DESCRIPTION", "Example FastAPI application"),
)


app = FastAPI(
    lifespan=lifespan,
    title=app_config.name,
    description=app_config.description,
    version=app_config.version,
)


@app.get("/ping")
async def ping_server():
    return {"message": "pong"}


app.include_router(system_router)
app.include_router(territory_router)
