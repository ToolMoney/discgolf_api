"""add unique constraint to username

Revision ID: 8888bc43f1d8
Revises: fa1965f1eda1
Create Date: 2023-07-20 16:29:01.736770

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = '8888bc43f1d8'
down_revision = 'fa1965f1eda1'
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table('user') as batch_op:
        batch_op.create_unique_constraint('unique_name', ['name'])


def downgrade() -> None:
    with op.batch_alter_table('user') as batch_op:
        batch_op.drop_constraint('unique_name', type_='unique')
