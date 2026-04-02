from fastapi import FastAPI

from __version__ import APP_VERSION
from test_routers import test_router

app = FastAPI(version=APP_VERSION, title="Example App", description="Some description")

app.include_router(test_router)


@app.get("/")
def get_root():
    return "root"
