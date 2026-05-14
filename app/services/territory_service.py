from collections.abc import Sequence

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.dto.territory_dto import TerritoryCreateDto, TerritoryDto, TerritoryUpdateDto

TERRITORY_RETURNING_COLUMNS = """
    id,
    name,
    territory_type,
    level,
    parent_id,
    code,
    description,
    area_sq_km,
    population
"""


class TerritoryService:
    async def create_territory(
        self,
        session: AsyncSession,
        territory: TerritoryCreateDto,
    ) -> TerritoryDto:
        result = await session.execute(
            text(
                """
                INSERT INTO territories (
                    name,
                    territory_type,
                    level,
                    parent_id,
                    code,
                    description,
                    area_sq_km,
                    population,
                    geom
                )
                VALUES (
                    :name,
                    :territory_type,
                    :level,
                    :parent_id,
                    :code,
                    :description,
                    :area_sq_km,
                    :population,
                    ST_GeomFromText(:geom_wkt, 4326)
                )
                RETURNING
                    """
                + TERRITORY_RETURNING_COLUMNS
                + """
                """
            ),
            territory.model_dump(),
        )
        row = result.mappings().one()
        return TerritoryDto.model_validate(dict(row))

    async def create_territories(
        self,
        session: AsyncSession,
        territories: Sequence[TerritoryCreateDto],
    ) -> list[TerritoryDto]:
        created = []
        for territory in territories:
            created.append(await self.create_territory(session, territory))
        await session.commit()
        return created

    async def update_territory(
        self,
        session: AsyncSession,
        territory_id: int,
        territory: TerritoryUpdateDto,
    ) -> TerritoryDto | None:
        update_data = territory.model_dump(exclude_unset=True)
        if not update_data:
            return await self.get_territory(session, territory_id)

        set_clauses = []
        params = {"territory_id": territory_id}
        for field_name, value in update_data.items():
            if field_name == "geom_wkt":
                set_clauses.append("geom = ST_GeomFromText(:geom_wkt, 4326)")
                params[field_name] = value
                continue
            set_clauses.append(f"{field_name} = :{field_name}")
            params[field_name] = value

        result = await session.execute(
            text(
                f"""
                UPDATE territories
                SET {", ".join(set_clauses)}
                WHERE id = :territory_id
                RETURNING {TERRITORY_RETURNING_COLUMNS}
                """
            ),
            params,
        )
        row = result.mappings().one_or_none()
        if row is None:
            await session.rollback()
            return None
        await session.commit()
        return TerritoryDto.model_validate(dict(row))

    async def delete_territory(
        self,
        session: AsyncSession,
        territory_id: int,
    ) -> int:
        result = await session.execute(
            text("DELETE FROM territories WHERE id = :territory_id"),
            {"territory_id": territory_id},
        )
        deleted = result.rowcount or 0
        await session.commit()
        return deleted

    async def get_territory(
        self,
        session: AsyncSession,
        territory_id: int,
    ) -> TerritoryDto | None:
        result = await session.execute(
            text(
                f"""
                SELECT {TERRITORY_RETURNING_COLUMNS}
                FROM territories
                WHERE id = :territory_id
                """
            ),
            {"territory_id": territory_id},
        )
        row = result.mappings().one_or_none()
        if row is None:
            return None
        return TerritoryDto.model_validate(dict(row))
