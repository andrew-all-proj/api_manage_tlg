"""add table feedback bots3

Revision ID: 1bf3bda7c7eb
Revises: 2e2ddd6bd83b
Create Date: 2023-04-04 15:25:05.128367

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1bf3bda7c7eb'
down_revision = '2e2ddd6bd83b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('users_to_feedback_bot_id_feedback_bot_fkey', 'users_to_feedback_bot', type_='foreignkey')
    op.create_foreign_key(None, 'users_to_feedback_bot', 'feedback_bots', ['id_feedback_bot'], ['id_feedback_bot'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users_to_feedback_bot', type_='foreignkey')
    op.create_foreign_key('users_to_feedback_bot_id_feedback_bot_fkey', 'users_to_feedback_bot', 'users', ['id_feedback_bot'], ['id_user'])
    # ### end Alembic commands ###
