from typing import Annotated

from fastapi import APIRouter, Depends, UploadFile


from app.dto.my_first_dto import MyFirstDto, SecondDto
from app.dependencies.dependenceis import get_system_service


system_router = APIRouter(prefix="/system", tags=["system"])


@system_router.get("/config/get_env")
async def get_env(
    env_key: str,
    system_service = Depends(get_system_service)
    ):
    
    result = await system_service.get_config(env_key)
    return result

@system_router.get("/config/get_available_env_keys")
async def get_available_env_keys(
    system_service = Depends(get_system_service)
):

    return await system_service.get_env_keys()

@system_router.put("/config/set_env")
async def set_env(
    env_key: str,
    env_value: str,
    system_service = Depends(get_system_service)
    ):

    await system_service.set_config(env_key, env_value)
    new_value = await system_service.get_config(env_key)
    return {"message": f"Environment variable {env_key} set to {new_value}"}

@system_router.post("/test_dto", response_model=str)
async def get_my_dto(
    file: UploadFile,
    user_id: int
) -> str:

    file_name = file.filename
    content = await file.read()
    return str(user_id) + file_name
