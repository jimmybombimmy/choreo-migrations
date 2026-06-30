"""Add users table

Revision ID: b3db3cf06450
Revises: be4b3f0344b1
Create Date: 2026-06-30 20:14:59.130722

"""

from typing import Sequence, Union

from alembic import op
from sqlalchemy import Column, UUID, VARCHAR, TIMESTAMP, func, ARRAY, ForeignKey

# revision identifiers, used by Alembic.
revision: str = "b3db3cf06450"
down_revision: Union[str, Sequence[str], None] = "be4b3f0344b1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# This will definitely need better authentication in the future
def upgrade() -> None:
    """Add users table."""
    op.create_table(
        "users",
        Column("id", UUID, primary_key=True),
        Column("username", VARCHAR(30), nullable=False),
        Column("email", VARCHAR(254), nullable=False),
        Column("password", VARCHAR(30), nullable=False),
        Column("created_at", TIMESTAMP, server_default=func.now(), nullable=False),
        Column("updated_at", TIMESTAMP),
        Column("collection_ids", ARRAY(UUID)),  # UUIDs of "collections.id"
    )
    pass


def downgrade() -> None:
    """Remove users table."""
    op.drop_table("users")
    pass
