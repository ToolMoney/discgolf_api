"""add user id columns

Revision ID: fa1965f1eda1
Revises: 1ad094e1f8ed
Create Date: 2023-07-18 15:17:43.608736

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fa1965f1eda1'
down_revision = '1ad094e1f8ed'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('course', sa.Column('user_id', sa.Integer(), nullable=True))
    with op.batch_alter_table("course") as batch_op:
        batch_op.create_foreign_key('fk_course_user', 'user', ['user_id'], ['id'])
    op.execute("UPDATE course SET user_id = 1")
    with op.batch_alter_table("course") as batch_op:
        batch_op.alter_column(
            'user_id',
            existing_type=sa.INTEGER(),
            nullable=False)

    op.add_column('disc', sa.Column('user_id', sa.Integer(), nullable=True))
    with op.batch_alter_table("disc") as batch_op:
        batch_op.create_foreign_key('fk_disc_user', 'user', ['user_id'], ['id'])
    op.execute("UPDATE disc SET user_id = 1")
    with op.batch_alter_table("disc") as batch_op:
        batch_op.alter_column(
            'user_id',
            existing_type=sa.INTEGER(),
            nullable=False)

    op.add_column('hole', sa.Column('user_id', sa.Integer(), nullable=True))
    with op.batch_alter_table("hole") as batch_op:
        batch_op.create_foreign_key('fk_hole_user', 'user', ['user_id'], ['id'])
    op.execute("UPDATE hole SET user_id = 1")
    with op.batch_alter_table("hole") as batch_op:
        batch_op.alter_column(
            'user_id',
            existing_type=sa.INTEGER(),
            nullable=False)

    op.add_column('round', sa.Column('user_id', sa.Integer(), nullable=True))
    with op.batch_alter_table("round") as batch_op:
        batch_op.create_foreign_key('fk_round_user', 'user', ['user_id'], ['id'])
    op.execute("UPDATE round SET user_id = 1")
    with op.batch_alter_table("round") as batch_op:
        batch_op.alter_column(
            'user_id',
            existing_type=sa.INTEGER(),
            nullable=False)

    op.add_column('score', sa.Column('user_id', sa.Integer(), nullable=True))
    with op.batch_alter_table("score") as batch_op:
        batch_op.create_foreign_key('fk_score_user', 'user', ['user_id'], ['id'])
    op.execute("UPDATE score SET user_id = 1")
    with op.batch_alter_table("score") as batch_op:
        batch_op.alter_column(
            'user_id',
            existing_type=sa.INTEGER(),
            nullable=False)


def downgrade() -> None:
    with op.batch_alter_table("score") as batch_op:
        batch_op.drop_constraint('fk_score_user', type_='foreignkey')
    op.drop_column('score', 'user_id')

    with op.batch_alter_table("round") as batch_op:
        batch_op.drop_constraint('fk_round_user', type_='foreignkey')
    op.drop_column('round', 'user_id')

    with op.batch_alter_table("hole") as batch_op:
        batch_op.drop_constraint('fk_hole_user', type_='foreignkey')
    op.drop_column('hole', 'user_id')

    with op.batch_alter_table("disc") as batch_op:
        batch_op.drop_constraint('fk_disc_user', type_='foreignkey')
    op.drop_column('disc', 'user_id')

    with op.batch_alter_table("course") as batch_op:
        batch_op.drop_constraint('fk_course_user', type_='foreignkey')
    op.drop_column('course', 'user_id')
