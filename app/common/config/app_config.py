from dataclasses import dataclass


@dataclass(frozen=True)
class FastApiAppConfig:
    version: str = "0.1.0"
    name: str = "Example FastAPI App"
    description: str = "Example FastAPI application"
