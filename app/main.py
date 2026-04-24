import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from app.__version__ import APP_VERSION
from app.routers.system_router import system_router
from app.common.config.app_config import FastApiAppConfig
from app.dependencies.init_dependencies import init_dependencies

@asynccontextmanager
async def lifespan(app: FastAPI):
    
    deps = init_dependencies()
    print(deps)
    yield
    print("App is shutted down")

app_config = FastApiAppConfig(
    version=os.environ.get("APP_VERSION"),
    name=os.environ.get("APP_NAME"),
    description=os.environ.get("APP_DESCRIPTION")
)


app = FastAPI(
    lifespan=lifespan,
    title=app_config.name,
    description=app_config.description,
    version=app_config.version
)


# @app.get("/")
# async def get_root():
#     return RedirectResponse("/docs")

@app.get("/ping")
async def ping_server():
    return "pong"

app.include_router(system_router)
