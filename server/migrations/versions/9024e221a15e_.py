"""empty message

Revision ID: 9024e221a15e
Revises: b9713af7d7bc
Create Date: 2021-12-22 13:31:34.840976

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9024e221a15e'
down_revision = 'b9713af7d7bc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('action',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=80), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_column('goal_message', 'type')
    op.add_column('log', sa.Column('title', sa.String(length=100), nullable=False))
    op.alter_column('log', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('log', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.drop_column('log', 'title')
    op.add_column('goal_message', sa.Column('type', sa.VARCHAR(length=80), autoincrement=False, nullable=False))
    op.drop_table('action')
    # ### end Alembic commands ###
