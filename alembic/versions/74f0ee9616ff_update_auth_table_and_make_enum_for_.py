"""update auth table and make enum for user and auth table

Revision ID: 74f0ee9616ff
Revises: 31556550e83b
Create Date: 2025-12-08 16:32:30.793162
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '74f0ee9616ff'
down_revision: Union[str, Sequence[str], None] = '31556550e83b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # 1️⃣ Create enums first
    userrole = sa.Enum('USER', 'SUPER_ADMIN', name='userrole')
    userrole.create(op.get_bind(), checkfirst=True)

    authenticationstatus = sa.Enum('PENDING', 'EXPIRED', 'CANCELED', 'SUCCESS', name='authenticationstatus')
    authenticationstatus.create(op.get_bind(), checkfirst=True)

    # 2️⃣ Add columns using the enums
    # If table already has data, provide a server_default
    op.add_column(
        'user',
        sa.Column('role', userrole, nullable=False, server_default='USER')
    )
    op.add_column(
        'userauthentication',
        sa.Column('authentication_status', authenticationstatus, nullable=False, server_default='PENDING')
    )

    # 3️⃣ Remove server defaults if you don't want them permanently
    op.alter_column('user', 'role', server_default=None)
    op.alter_column('userauthentication', 'authentication_status', server_default=None)


def downgrade() -> None:
    """Downgrade schema."""

    # 1️⃣ Drop columns first
    op.drop_column('userauthentication', 'authentication_status')
    op.drop_column('user', 'role')

    # 2️⃣ Drop enum types
    userrole = sa.Enum('USER', 'SUPER_ADMIN', name='userrole')
    userrole.drop(op.get_bind(), checkfirst=True)

    authenticationstatus = sa.Enum('PENDING', 'EXPIRED', 'CANCELED', 'SUCCESS', name='authenticationstatus')
    authenticationstatus.drop(op.get_bind(), checkfirst=True)
