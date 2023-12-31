"""initial migration

Revision ID: db53f681fb31
Revises:
Create Date: 2023-07-05 13:03:00.567527

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'db53f681fb31'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'course',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('location', sa.String(), nullable=True),
        sa.Column('fee', sa.Integer(), nullable=True),
        sa.Column('favorite', sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'disc',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('speed', sa.Integer(), nullable=True),
        sa.Column('glide', sa.Integer(), nullable=True),
        sa.Column('turn', sa.Integer(), nullable=True),
        sa.Column('fade', sa.Integer(), nullable=True),
        sa.Column('inBag', sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'hole',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('hole_number', sa.Integer(), nullable=True),
        sa.Column('par', sa.Integer(), nullable=True),
        sa.Column('layout', sa.String(), nullable=True),
        sa.Column('distance', sa.Integer(), nullable=True),
        sa.Column('course_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['course_id'], ['course.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'round',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('date', sa.String(), nullable=True),
        sa.Column('default_layout', sa.String(), nullable=True),
        sa.Column('course_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['course_id'], ['course.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'score',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('round_id', sa.Integer(), nullable=True),
        sa.Column('hole_id', sa.Integer(), nullable=True),
        sa.Column('score', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['hole_id'], ['hole.id'], ),
        sa.ForeignKeyConstraint(['round_id'], ['round.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('score')
    op.drop_table('round')
    op.drop_table('hole')
    op.drop_table('disc')
    op.drop_table('course')
