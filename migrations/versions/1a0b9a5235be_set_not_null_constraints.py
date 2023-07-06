"""set not null constraints

Revision ID: 1a0b9a5235be
Revises: a81d3341fe6b
Create Date: 2023-07-05 14:48:24.557541

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1a0b9a5235be'
down_revision = 'a81d3341fe6b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("DELETE FROM hole WHERE course_id IS NULL;")
    with op.batch_alter_table("hole") as batch_op:
        batch_op.alter_column('course_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.execute("DELETE FROM round WHERE course_id IS NULL;")
    with op.batch_alter_table("round") as batch_op:
        batch_op.alter_column('course_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.execute("DELETE FROM score WHERE round_id IS NULL;")
    with op.batch_alter_table("score") as batch_op:
        batch_op.alter_column('round_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.execute("DELETE FROM score WHERE hole_id IS NULL;")
    with op.batch_alter_table("score") as batch_op:
        batch_op.alter_column('hole_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.execute("DELETE FROM score WHERE score IS NULL;")
    with op.batch_alter_table("score") as batch_op:
        batch_op.alter_column('score',
               existing_type=sa.INTEGER(),
               nullable=False)


def downgrade() -> None:
    with op.batch_alter_table("hole") as batch_op:
        batch_op.alter_column('course_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    with op.batch_alter_table("round") as batch_op:
        batch_op.alter_column('course_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    with op.batch_alter_table("score") as batch_op:
        batch_op.alter_column('round_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    with op.batch_alter_table("score") as batch_op:
        batch_op.alter_column('hole_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    with op.batch_alter_table("score") as batch_op:
        batch_op.alter_column('score',
               existing_type=sa.INTEGER(),
               nullable=True)