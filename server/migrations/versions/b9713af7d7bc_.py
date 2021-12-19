"""empty message

Revision ID: b9713af7d7bc
Revises: a12121db403c
Create Date: 2021-12-19 15:56:42.466657

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b9713af7d7bc'
down_revision = 'a12121db403c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('goal_message', sa.Column('description', sa.Text(), nullable=True))
    op.add_column('goal_message', sa.Column('completed', sa.Boolean(), nullable=False))
    op.drop_column('goal_message', 'text')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('goal_message', sa.Column('text', sa.TEXT(), autoincrement=False, nullable=True))
    op.drop_column('goal_message', 'completed')
    op.drop_column('goal_message', 'description')
    # ### end Alembic commands ###