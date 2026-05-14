from fastapi import APIRouter, Depends, HTTPException, UploadFile

from app.dependencies.dependencies import get_system_service

system_router = APIRouter(prefix="/system", tags=["system"])


@system_router.get("/config/get_env")
async def get_env(
    env_key: str,
    system_service=Depends(get_system_service),
):
    try:
        return await system_service.get_config(env_key)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@system_router.get("/config/get_available_env_keys")
async def get_available_env_keys(
    system_service=Depends(get_system_service),
):
    return await system_service.get_env_keys()


@system_router.put("/config/set_env")
async def set_env(
    env_key: str,
    env_value: str,
    system_service=Depends(get_system_service),
):
    await system_service.set_config(env_key, env_value)
    new_value = await system_service.get_config(env_key)
    return {"message": f"Environment variable {env_key} set to {new_value}"}


@system_router.post("/test_dto", response_model=str)
async def get_my_dto(
    file: UploadFile,
    user_id: int,
) -> str:
    await file.read()
    return f"{user_id}{file.filename}"
