from app.common.db import get_async_session
from app.dependencies.init_dependencies import app_dependencies


def get_system_service():
    return app_dependencies["system_service"]


__all__ = ["get_async_session", "get_system_service"]
