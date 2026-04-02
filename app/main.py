import os

from fastapi import FastAPI

from app.__version__ import APP_VERSION
from app.routers.system_router import system_router
from app.common.config.app_config import FastApiAppConfig

app_config = FastApiAppConfig(
    version=os.environ.get("APP_VERSION"),
    name=os.environ.get("APP_NAME"),
    description=os.environ.get("APP_DESCRIPTION")
)


app = FastAPI(
    title=app_config.name,
    description=app_config.description,
    version=app_config.version
)


@app.get("/")
async def get_root():
    return "root"

app.include_router(system_router)
