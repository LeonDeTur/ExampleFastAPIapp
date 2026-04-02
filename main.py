from fastapi import FastAPI

from test_routers import test_router
from __version__ import APP_VERSION


app = FastAPI(version=APP_VERSION, title="Example App", description="Some description")

app.include_router(test_router)


@app.get("/")
def get_root():
    return "root"
