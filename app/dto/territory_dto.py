from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, Field

TerritoryType = Literal["city", "district", "municipality"]


class TerritoryCreateDto(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    territory_type: TerritoryType | str = Field(max_length=100)
    level: int = Field(ge=1)
    parent_id: int | None = None
    code: str | None = Field(default=None, max_length=50)
    description: str | None = None
    area_sq_km: Decimal | None = Field(default=None, ge=0)
    population: int | None = Field(default=None, ge=0)
    geom_wkt: str = Field(
        min_length=1,
        description="Geometry in WKT MULTIPOLYGON format, SRID 4326",
        examples=[
            "MULTIPOLYGON(((30.10 59.80,30.55 59.80,30.55 60.10,30.10 60.10,30.10 59.80)))"
        ],
    )


class TerritoryUpdateDto(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    territory_type: TerritoryType | str | None = Field(default=None, max_length=100)
    level: int | None = Field(default=None, ge=1)
    parent_id: int | None = None
    code: str | None = Field(default=None, max_length=50)
    description: str | None = None
    area_sq_km: Decimal | None = Field(default=None, ge=0)
    population: int | None = Field(default=None, ge=0)
    geom_wkt: str | None = Field(
        default=None,
        min_length=1,
        description="Geometry in WKT MULTIPOLYGON format, SRID 4326",
    )


class TerritoryDto(BaseModel):
    id: int
    name: str
    territory_type: str
    level: int
    parent_id: int | None = None
    code: str | None = None
    description: str | None = None
    area_sq_km: Decimal | None = None
    population: int | None = None


class TerritoryUploadResultDto(BaseModel):
    inserted: int
    territories: list[TerritoryDto]


class TerritoryDeleteResultDto(BaseModel):
    deleted: int
