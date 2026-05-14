import os


class SystemService:
    async def get_config(self, key: str) -> str:
        result = os.environ.get(key)
        if result is not None:
            return result
        raise KeyError(f"Key {key} not found in environment variables")

    async def set_config(self, key: str, value: str) -> None:
        os.environ[key] = value

    async def get_env_keys(self) -> list[str]:
        return sorted(key for key in os.environ if key.startswith("APP_"))


system_service = SystemService()
