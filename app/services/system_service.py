import os


class SystemService:
    
    def __init__(self):
        
        pass
    
    async def get_config(self, key: str):
        
        result = os.environ.get(key)
        if result:
            return result
        else:
            raise KeyError(f"Key {key} not found in environment variables")
    
    def set_config(self, key: str, value: str):
        
        self.get_config(key)
        os.environ[key] = value

    def get_env_keys(self):
        
        return [key for key in list(os.environ.keys()) if "APP_" in key]
    

system_service = SystemService()
