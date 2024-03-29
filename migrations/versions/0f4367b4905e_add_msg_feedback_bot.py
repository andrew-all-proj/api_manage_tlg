"""add msg feedback bot

Revision ID: 0f4367b4905e
Revises: 09f3ff4750d6
Create Date: 2023-04-08 12:08:22.811160

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0f4367b4905e'
down_revision = '09f3ff4750d6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ban_users_feedback_bot',
    sa.Column('id_ban_users_feedback_bot', sa.Integer(), nullable=False),
    sa.Column('id_user_telegram', sa.Integer(), nullable=False),
    sa.Column('id_feedback_bot', sa.Integer(), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['id_feedback_bot'], ['feedback_bots.id_feedback_bot'], ),
    sa.PrimaryKeyConstraint('id_ban_users_feedback_bot')
    )
    op.create_table('msg_feedback_bots',
    sa.Column('id_msg_feedback_bots', sa.Integer(), nullable=False),
    sa.Column('id_incoming_msg', sa.Integer(), nullable=False),
    sa.Column('id_incoming_user', sa.Integer(), nullable=False),
    sa.Column('id_incoming_chat', sa.Integer(), nullable=False),
    sa.Column('id_feedback_bot', sa.Integer(), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['id_feedback_bot'], ['feedback_bots.id_feedback_bot'], ),
    sa.PrimaryKeyConstraint('id_msg_feedback_bots')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('msg_feedback_bots')
    op.drop_table('ban_users_feedback_bot')
    # ### end Alembic commands ###
