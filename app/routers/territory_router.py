import csv
import json
from io import StringIO

from fastapi import APIRouter, Depends, HTTPException, UploadFile
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.dependencies import get_async_session
from app.dto.territory_dto import (
    TerritoryCreateDto,
    TerritoryDeleteResultDto,
    TerritoryDto,
    TerritoryUpdateDto,
    TerritoryUploadResultDto,
)
from app.services.territory_service import TerritoryService

territory_router = APIRouter(prefix="/territories", tags=["territories"])
territory_service = TerritoryService()


@territory_router.post("", response_model=TerritoryDto, status_code=201)
async def create_territory(
    territory: TerritoryCreateDto,
    session: AsyncSession = Depends(get_async_session),
):
    try:
        created = await territory_service.create_territories(session, [territory])
    except SQLAlchemyError as exc:
        await session.rollback()
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return created[0]


@territory_router.post(
    "/bulk", response_model=TerritoryUploadResultDto, status_code=201
)
async def create_territories(
    territories: list[TerritoryCreateDto],
    session: AsyncSession = Depends(get_async_session),
):
    try:
        created = await territory_service.create_territories(session, territories)
    except SQLAlchemyError as exc:
        await session.rollback()
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return TerritoryUploadResultDto(inserted=len(created), territories=created)


@territory_router.post(
    "/upload", response_model=TerritoryUploadResultDto, status_code=201
)
async def upload_territories(
    file: UploadFile,
    session: AsyncSession = Depends(get_async_session),
):
    raw_content = (await file.read()).decode("utf-8-sig")
    territories = parse_territory_file(file.filename or "", raw_content)

    try:
        created = await territory_service.create_territories(session, territories)
    except SQLAlchemyError as exc:
        await session.rollback()
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return TerritoryUploadResultDto(inserted=len(created), territories=created)


@territory_router.patch("/{territory_id}", response_model=TerritoryDto)
async def update_territory(
    territory_id: int,
    territory: TerritoryUpdateDto,
    session: AsyncSession = Depends(get_async_session),
):
    try:
        updated = await territory_service.update_territory(
            session, territory_id, territory
        )
    except SQLAlchemyError as exc:
        await session.rollback()
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    if updated is None:
        raise HTTPException(
            status_code=404, detail=f"Territory {territory_id} not found"
        )
    return updated


@territory_router.delete("/{territory_id}", response_model=TerritoryDeleteResultDto)
async def delete_territory(
    territory_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    try:
        deleted = await territory_service.delete_territory(session, territory_id)
    except SQLAlchemyError as exc:
        await session.rollback()
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    if deleted == 0:
        raise HTTPException(
            status_code=404, detail=f"Territory {territory_id} not found"
        )
    return TerritoryDeleteResultDto(deleted=deleted)


def parse_territory_file(filename: str, raw_content: str) -> list[TerritoryCreateDto]:
    if filename.lower().endswith(".csv"):
        return parse_csv_territories(raw_content)
    return parse_json_territories(raw_content)


def parse_json_territories(raw_content: str) -> list[TerritoryCreateDto]:
    try:
        payload = json.loads(raw_content)
    except json.JSONDecodeError as exc:
        raise HTTPException(status_code=400, detail="Invalid JSON file") from exc

    if isinstance(payload, dict):
        payload = [payload]
    if not isinstance(payload, list):
        raise HTTPException(
            status_code=400, detail="JSON file must contain an object or an array"
        )
    try:
        return [TerritoryCreateDto.model_validate(item) for item in payload]
    except ValidationError as exc:
        raise HTTPException(status_code=400, detail=exc.errors()) from exc


def parse_csv_territories(raw_content: str) -> list[TerritoryCreateDto]:
    rows = csv.DictReader(StringIO(raw_content))
    if not rows.fieldnames:
        raise HTTPException(status_code=400, detail="CSV file is empty")
    try:
        return [
            TerritoryCreateDto.model_validate(normalize_csv_row(row)) for row in rows
        ]
    except ValidationError as exc:
        raise HTTPException(status_code=400, detail=exc.errors()) from exc


def normalize_csv_row(row: dict[str, str | None]) -> dict[str, str | None]:
    return {
        key: value if value != "" else None
        for key, value in row.items()
        if key is not None
    }
