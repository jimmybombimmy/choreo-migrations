"""Add users and user_task_list_memberships tables

Revision ID: b3db3cf06450
Revises: be4b3f0344b1
Create Date: 2026-06-30 20:14:59.130722

"""

from typing import Sequence, Union

from alembic import op
from sqlalchemy import (
    Column,
    UUID,
    VARCHAR,
    TIMESTAMP,
    func,
    ForeignKey,
    UniqueConstraint,
    Enum,
)

# revision identifiers, used by Alembic.
revision: str = "b3db3cf06450"
down_revision: Union[str, Sequence[str], None] = "be4b3f0344b1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# This will definitely need better authentication in the future
def upgrade() -> None:
    """
    Add "users" table.

    Add "user_task_list_membership" to link many-to-many unique relationships between users and task_lists.
    This will be to allow users to get their task list and see other users that have access.
    """

    op.create_table(
        "users",
        Column("id", UUID(as_uuid=True), primary_key=True),
        Column("username", VARCHAR(30), nullable=False),
        Column("email", VARCHAR(254), nullable=False),
        Column("password", VARCHAR(30), nullable=False),
        Column("created_at", TIMESTAMP, server_default=func.now(), nullable=False),
        Column("updated_at", TIMESTAMP),
    )
    op.create_table(
        "user_task_list_memberships",
        Column(
            "user_id",
            UUID(as_uuid=True),
            ForeignKey("users.id", ondelete="CASCADE", name="fk_utlm_user"),
            primary_key=True,
        ),
        Column(
            "task_list_id",
            UUID(as_uuid=True),
            ForeignKey("task_lists.id", ondelete="CASCADE", name="fk_utlm_task_list"),
            primary_key=True,
        ),
        Column(
            "role",
            Enum(
                "viewer",
                "editor",
                "admin",
                "superadmin",
                name="utlm_roles",
            ),
            nullable=False,
            default="viewer",
            server_default="viewer",
        ),
        Column("created_at", TIMESTAMP, server_default=func.now(), nullable=False),
        Column("updated_at", TIMESTAMP),
        UniqueConstraint(
            "user_id",
            "task_list_id",
            name="uq_user_task_list_membership",
        ),
    )


def downgrade() -> None:
    """Remove users table."""
    op.drop_table("user_task_list_memberships")
    op.drop_table("users")

    op.execute("DROP TYPE utlm_roles")
