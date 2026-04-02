from fastapi import APIRouter

from app.services.system_service import system_service


system_router = APIRouter(prefix="/system", tags=["system"])


@system_router.get("/config/get_env")
async def get_env(env_key: str):
    
    result = await system_service.get_config(env_key)
    return result

@system_router.get("/config/get_available_env_keys")
async def get_available_env_keys():

    return await system_service.get_env_keys()

@system_router.put("/config/set_env")
async def set_env(env_key: str, env_value: str):

    await system_service.set_config(env_key, env_value)
    new_value = await system_service.get_config(env_key)
    return {"message": f"Environment variable {env_key} set to {new_value}"}
