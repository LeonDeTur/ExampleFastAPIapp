"""Initial migration

Revision ID: 4bae3770ee79
Revises: 
Create Date: 2026-04-24 16:02:43.969760

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from geoalchemy2 import Geometry



# revision identifiers, used by Alembic.
revision: str = '4bae3770ee79'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS postgis")

    op.create_table(
        "territories",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("territory_type", sa.String(length=100), nullable=False),
        sa.Column("level", sa.Integer(), nullable=False),
        sa.Column("parent_id", sa.Integer(), nullable=True),
        sa.Column("code", sa.String(length=50), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("area_sq_km", sa.Numeric(12, 3), nullable=True),
        sa.Column("population", sa.Integer(), nullable=True),
        sa.Column("geom", Geometry(geometry_type="MULTIPOLYGON", srid=4326), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.ForeignKeyConstraint(["parent_id"], ["territories.id"], ondelete="SET NULL"),
    )
    
    op.create_index(
        "idx_territories_type",
        "territories",
        ["territory_type"],
    )

    op.create_index(
        "idx_territories_level",
        "territories",
        ["level"],
    )

    op.execute("""
        INSERT INTO territories (
            id,
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
        VALUES
        (
            1,
            'Санкт-Петербург',
            'city',
            1,
            NULL,
            'SPB',
            'Город федерального значения',
            1439.00,
            5600000,
            ST_GeomFromText(
                'MULTIPOLYGON(((
                    30.10 59.80,
                    30.55 59.80,
                    30.55 60.10,
                    30.10 60.10,
                    30.10 59.80
                )))',
                4326
            )
        ),
        (
            2,
            'Центральный район',
            'district',
            2,
            1,
            'SPB-CENTRAL',
            'Внутригородской район Санкт-Петербурга',
            17.10,
            220000,
            ST_GeomFromText(
                'MULTIPOLYGON(((
                    30.30 59.91,
                    30.38 59.91,
                    30.38 59.96,
                    30.30 59.96,
                    30.30 59.91
                )))',
                4326
            )
        ),
        (
            3,
            'Адмиралтейский район',
            'district',
            2,
            1,
            'SPB-ADMIRAL',
            'Внутригородской район Санкт-Петербурга',
            13.82,
            160000,
            ST_GeomFromText(
                'MULTIPOLYGON(((
                    30.25 59.90,
                    30.33 59.90,
                    30.33 59.94,
                    30.25 59.94,
                    30.25 59.90
                )))',
                4326
            )
        ),
        (
            4,
            'МО Литейный округ',
            'municipality',
            3,
            2,
            'SPB-CENTRAL-LITEINY',
            'Муниципальное образование внутри Центрального района',
            2.40,
            45000,
            ST_GeomFromText(
                'MULTIPOLYGON(((
                    30.33 59.93,
                    30.36 59.93,
                    30.36 59.95,
                    30.33 59.95,
                    30.33 59.93
                )))',
                4326
            )
        );
    """)


def downgrade() -> None:
    op.drop_index("idx_territories_level", table_name="territories")
    op.drop_index("idx_territories_type", table_name="territories")
    op.drop_index("idx_territories_geom", table_name="territories")

    op.drop_table("territories")
