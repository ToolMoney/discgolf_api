"""corrected inBag to snake case

Revision ID: a81d3341fe6b
Revises: db53f681fb31
Create Date: 2023-07-05 14:02:49.304164

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = 'a81d3341fe6b'
down_revision = 'db53f681fb31'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column('disc', 'inBag', new_column_name='in_bag')


def downgrade() -> None:
    op.alter_column('disc', 'in_bag', new_column_name='inBag')
