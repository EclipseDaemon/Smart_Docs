"""add gin index on search vector

Revision ID: b5ed70c18c48
Revises: e9b8a365e086
Create Date: 2026-03-23 10:57:04.410148

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b5ed70c18c48'
down_revision: Union[str, Sequence[str], None] = 'e9b8a365e086'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        "CREATE INDEX idx_documents_search_vector "
        "ON documents USING GIN(search_vector)"
    )


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS idx_documents_search_vector")