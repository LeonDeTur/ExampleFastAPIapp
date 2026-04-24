from typing import Any

from app.services.system_service import SystemService

app_dependencies: dict[str, Any] = {}

def init_dependencies():
    
    app_dependencies["system_service"] = SystemService()
    return app_dependencies
