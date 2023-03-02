"""constraction event

Revision ID: fac77d8a8acc
Revises: 314b44eb3b4c
Create Date: 2023-03-02 08:21:10.020099

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fac77d8a8acc'
down_revision = '314b44eb3b4c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('_id_post_date_start_uc', 'events', ['id_post', 'date_start'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('_id_post_date_start_uc', 'events', type_='unique')
    # ### end Alembic commands ###
