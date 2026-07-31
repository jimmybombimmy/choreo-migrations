"""create initial tables

Revision ID: be4b3f0344b1
Revises:
Create TIMESTAMP: 2026-06-24 21:10:54.927145

"""

from typing import Sequence, Union

from alembic import op
from sqlalchemy import Column, UUID, VARCHAR, TIMESTAMP, ForeignKey, BOOLEAN, func

# revision identifiers, used by Alembic.
revision: str = "be4b3f0344b1"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create initial tables."""
    op.create_table(
        "task_types",
        Column("id", UUID(as_uuid=True), primary_key=True),
        Column("name", VARCHAR(30), nullable=False),
        Column("description", VARCHAR(140)),
        Column("created_at", TIMESTAMP, server_default=func.now(), nullable=False),
        Column("updated_at", TIMESTAMP),
    )

    op.create_table(
        "collections",
        Column("id", UUID(as_uuid=True), primary_key=True),
        Column("name", VARCHAR(30), nullable=False),
        Column("description", VARCHAR(140)),
        Column("task_type_id", UUID(as_uuid=True), ForeignKey("task_types.id")),
        Column("created_at", TIMESTAMP, server_default=func.now(), nullable=False),
        Column("last_completed_at", TIMESTAMP),
        Column("updated_at", TIMESTAMP),
    )

    op.create_table(
        "task_lists",
        Column("id", UUID(as_uuid=True), primary_key=True),
        Column("name", VARCHAR(30), nullable=False),
        Column("collection_id", UUID(as_uuid=True), ForeignKey("collections.id")),
        Column("created_at", TIMESTAMP, server_default=func.now(), nullable=False),
        Column("last_completed_at", TIMESTAMP),
        Column("updated_at", TIMESTAMP),
        Column("locked", BOOLEAN),
    )

    op.create_table(
        "tasks",
        Column("id", UUID(as_uuid=True), primary_key=True),
        Column("name", VARCHAR(30), nullable=False),
        Column("task_list_id", UUID(as_uuid=True), ForeignKey("task_lists.id")),
        Column("created_at", TIMESTAMP, server_default=func.now(), nullable=False),
        Column("last_completed_at", TIMESTAMP),
        Column("completed", BOOLEAN),
        Column("locked", BOOLEAN),
        Column("parent_task_id", UUID(as_uuid=True), ForeignKey("tasks.id")),
    )


def downgrade() -> None:
    """Remove initial tables."""
    op.drop_table("tasks")
    op.drop_table("task_lists")
    op.drop_table("collections")
    op.drop_table("task_types")
    pass
