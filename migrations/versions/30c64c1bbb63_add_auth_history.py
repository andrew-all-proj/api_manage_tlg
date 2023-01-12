"""add auth history

Revision ID: 30c64c1bbb63
Revises: 6ed7ef966f80
Create Date: 2023-01-12 14:51:02.521057

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '30c64c1bbb63'
down_revision = '6ed7ef966f80'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('auth_history',
    sa.Column('id_auth_history', sa.Integer(), nullable=False),
    sa.Column('id_user', sa.Integer(), nullable=False),
    sa.Column('date_auth', sa.DateTime(), nullable=False),
    sa.Column('from_is', sa.String(length=300), nullable=False),
    sa.ForeignKeyConstraint(['id_user'], ['users.id_user'], ),
    sa.PrimaryKeyConstraint('id_auth_history')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('auth_history')
    # ### end Alembic commands ###
