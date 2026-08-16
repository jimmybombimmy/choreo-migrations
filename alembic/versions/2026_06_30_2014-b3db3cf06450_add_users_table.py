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
    Enum,
)

# revision identifiers, used by Alembic.
revision: str = "b3db3cf06450"
down_revision: Union[str, Sequence[str], None] = "be4b3f0344b1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

invitation_status = Enum(
    "PENDING",
    "ACCEPTED",
    "DECLINED",
    "EXPIRED",
    name="invitation_status",
)

membership_roles = Enum(
    "VIEWER",  # can view but not tick anything
    "USER",  # can view and tick anything
    "EDITOR",  # can view, tick, add and delete tasks
    "ADMIN",  # editor + add and remove above roles
    "OWNER",  # admin + add and remove admin roles
    name="membership_roles",
)


# This will definitely need better authentication in the future
def upgrade() -> None:
    """
    Add "users" table.

    Add "user_task_list_membership" to link many-to-many unique relationships between users and task_lists.
    This will be to allow users to get their task list and see other users that have access.

    Add "user_collection_membership" to link similar to above

    Add "collection_task_list_membership" to link similar to above

    Add "user_id" column to collections (this doesn't need many-to-many)

    Add invitation tables for task_lists and collections so that users can invite other users to join
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
            membership_roles,
            nullable=False,
            server_default="VIEWER",
        ),
        Column("created_at", TIMESTAMP, server_default=func.now(), nullable=False),
        Column("updated_at", TIMESTAMP),
    )

    op.create_table(
        "collection_task_list_memberships",
        Column(
            "collection_id",
            UUID(as_uuid=True),
            ForeignKey("collections.id", ondelete="CASCADE", name="fk_ctlm_collection"),
            primary_key=True,
        ),
        Column(
            "task_list_id",
            UUID(as_uuid=True),
            ForeignKey("task_lists.id", ondelete="CASCADE", name="fk_ctlm_task_list"),
            primary_key=True,
        ),
        Column("created_at", TIMESTAMP, server_default=func.now(), nullable=False),
        Column("updated_at", TIMESTAMP),
    )

    op.create_table(
        "user_collection_memberships",
        Column(
            "collection_id",
            UUID(as_uuid=True),
            ForeignKey("collections.id", ondelete="CASCADE", name="fk_ucm_collection"),
            primary_key=True,
        ),
        Column(
            "user_id",
            UUID(as_uuid=True),
            ForeignKey("users.id", ondelete="CASCADE", name="fk_ucm_user"),
            primary_key=True,
        ),
        Column(
            "role",
            membership_roles,
            nullable=False,
            server_default="VIEWER",
        ),
        Column("created_at", TIMESTAMP, server_default=func.now(), nullable=False),
        Column("updated_at", TIMESTAMP),
    )

    op.create_table(
        "task_list_invitations",
        Column("id", UUID(as_uuid=True), primary_key=True),
        Column(
            "task_list_id",
            UUID(as_uuid=True),
            ForeignKey("task_lists.id", ondelete="CASCADE", name="fk_tli_task_list"),
            nullable=False,
        ),
        Column(
            "sender_id",
            UUID(as_uuid=True),
            ForeignKey("users.id", ondelete="CASCADE", name="fk_tli_sender"),
            nullable=False,
        ),
        Column(
            "recipient_id",
            UUID(as_uuid=True),
            ForeignKey("users.id", ondelete="CASCADE", name="fk_tli_recipient"),
            nullable=False,
        ),
        Column(
            "status",
            invitation_status,
            nullable=False,
            server_default="PENDING",
        ),
        Column("created_at", TIMESTAMP, server_default=func.now(), nullable=False),
        Column("updated_at", TIMESTAMP),
    )

    op.create_table(
        "collection_invitations",
        Column("id", UUID(as_uuid=True), primary_key=True),
        Column(
            "collection_id",
            UUID(as_uuid=True),
            ForeignKey("collections.id", ondelete="CASCADE", name="fk_ci_collection"),
            nullable=False,
        ),
        Column(
            "sender_id",
            UUID(as_uuid=True),
            ForeignKey("users.id", ondelete="CASCADE", name="fk_ci_sender"),
            nullable=False,
        ),
        Column(
            "recipient_id",
            UUID(as_uuid=True),
            ForeignKey("users.id", ondelete="CASCADE", name="fk_ci_recipient"),
            nullable=False,
        ),
        Column(
            "status",
            invitation_status,
            nullable=False,
            server_default="PENDING",
        ),
        Column("created_at", TIMESTAMP, server_default=func.now(), nullable=False),
        Column("updated_at", TIMESTAMP),
    )


def downgrade() -> None:
    """Remove users table."""
    op.drop_table("collection_invitations")
    op.drop_table("task_list_invitations")

    op.drop_table("collection_task_list_memberships")
    op.drop_table("user_task_list_memberships")
    op.drop_table("user_collection_memberships")

    op.drop_table("users")

    membership_roles.drop(op.get_bind(), checkfirst=True)
    invitation_status.drop(op.get_bind(), checkfirst=True)
