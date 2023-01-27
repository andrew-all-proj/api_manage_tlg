"""uniq pair user_chanel

Revision ID: 3d5fda11924a
Revises: c06e5d86279c
Create Date: 2023-01-23 10:23:03.273713

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3d5fda11924a'
down_revision = 'c06e5d86279c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('_user_channel_uc', 'users_channels', ['id_user', 'id_channel'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('_user_channel_uc', 'users_channels', type_='unique')
    # ### end Alembic commands ###