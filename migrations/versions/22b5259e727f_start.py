"""start

Revision ID: 22b5259e727f
Revises: 
Create Date: 2023-03-28 16:15:15.474698

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '22b5259e727f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('types_media',
    sa.Column('id_type_media', sa.Integer(), nullable=False),
    sa.Column('type_media', sa.String(length=20), nullable=False),
    sa.Column('name_dir', sa.String(length=250), nullable=False),
    sa.Column('extension', sa.String(length=20), nullable=False),
    sa.PrimaryKeyConstraint('id_type_media')
    )
    op.create_table('users',
    sa.Column('id_user', sa.Integer(), nullable=False),
    sa.Column('user_name', sa.String(length=30), nullable=False),
    sa.Column('id_telegram', sa.String(length=50), nullable=True),
    sa.Column('email', sa.String(length=50), nullable=False),
    sa.Column('confirmed', sa.Boolean(), nullable=False),
    sa.Column('password', sa.String(length=128), nullable=False),
    sa.Column('date_registration', sa.DateTime(), nullable=False),
    sa.Column('data_update', sa.DateTime(), nullable=False),
    sa.Column('role', sa.String(length=30), nullable=False),
    sa.Column('is_archive', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id_user'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('id_telegram')
    )
    op.create_table('auth_history',
    sa.Column('id_auth_history', sa.Integer(), nullable=False),
    sa.Column('id_user', sa.Integer(), nullable=False),
    sa.Column('date_auth', sa.DateTime(), nullable=False),
    sa.Column('from_is', sa.String(length=300), nullable=False),
    sa.ForeignKeyConstraint(['id_user'], ['users.id_user'], ),
    sa.PrimaryKeyConstraint('id_auth_history')
    )
    op.create_table('channels',
    sa.Column('id_channel', sa.Integer(), nullable=False),
    sa.Column('name_channel', sa.String(length=200), nullable=False),
    sa.Column('link_channel', sa.String(length=200), nullable=False),
    sa.Column('id_telegram', sa.String(length=200), nullable=False),
    sa.Column('date_create', sa.DateTime(), nullable=False),
    sa.Column('data_update', sa.DateTime(), nullable=False),
    sa.Column('is_archive', sa.Boolean(), nullable=False),
    sa.Column('id_user_admin', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_user_admin'], ['users.id_user'], ),
    sa.PrimaryKeyConstraint('id_channel'),
    sa.UniqueConstraint('id_telegram')
    )
    op.create_table('media_contents',
    sa.Column('id_media', sa.Integer(), nullable=False),
    sa.Column('id_type_media', sa.Integer(), nullable=False),
    sa.Column('name_file', sa.String(length=250), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('date_download', sa.DateTime(), nullable=False),
    sa.Column('last_time_used', sa.DateTime(), nullable=False),
    sa.Column('id_user', sa.Integer(), nullable=False),
    sa.Column('is_archive', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['id_type_media'], ['types_media.id_type_media'], ),
    sa.ForeignKeyConstraint(['id_user'], ['users.id_user'], ),
    sa.PrimaryKeyConstraint('id_media')
    )
    op.create_table('posts',
    sa.Column('id_post', sa.Integer(), nullable=False),
    sa.Column('text', sa.String(length=3000), nullable=True),
    sa.Column('id_user', sa.Integer(), nullable=False),
    sa.Column('date_create', sa.DateTime(), nullable=False),
    sa.Column('data_update', sa.DateTime(), nullable=False),
    sa.Column('is_archive', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['id_user'], ['users.id_user'], ),
    sa.PrimaryKeyConstraint('id_post')
    )
    op.create_table('events',
    sa.Column('id_event', sa.Integer(), nullable=False),
    sa.Column('id_post', sa.Integer(), nullable=False),
    sa.Column('id_message', sa.Integer(), nullable=True),
    sa.Column('id_channel', sa.Integer(), nullable=False),
    sa.Column('date_start', sa.DateTime(), nullable=False),
    sa.Column('date_stop', sa.DateTime(), nullable=True),
    sa.Column('completed', sa.Boolean(), nullable=False),
    sa.Column('published', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['id_channel'], ['channels.id_channel'], ),
    sa.ForeignKeyConstraint(['id_post'], ['posts.id_post'], ),
    sa.PrimaryKeyConstraint('id_event'),
    sa.UniqueConstraint('id_post', 'date_start', name='_id_post_date_start_uc')
    )
    op.create_table('posts_media',
    sa.Column('id_post', sa.Integer(), nullable=False),
    sa.Column('id_media', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_media'], ['media_contents.id_media'], ),
    sa.ForeignKeyConstraint(['id_post'], ['posts.id_post'], ),
    sa.PrimaryKeyConstraint('id_post', 'id_media')
    )
    op.create_table('tags',
    sa.Column('id_tag', sa.Integer(), nullable=False),
    sa.Column('tag_name', sa.String(length=50), nullable=False),
    sa.Column('id_channel', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['id_channel'], ['channels.id_channel'], ),
    sa.PrimaryKeyConstraint('id_tag'),
    sa.UniqueConstraint('tag_name', 'id_channel', name='_tag_channel_uc')
    )
    op.create_table('users_channels',
    sa.Column('id_user_channel', sa.Integer(), nullable=False),
    sa.Column('id_user', sa.Integer(), nullable=False),
    sa.Column('id_channel', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_channel'], ['channels.id_channel'], ),
    sa.ForeignKeyConstraint(['id_user'], ['users.id_user'], ),
    sa.PrimaryKeyConstraint('id_user_channel'),
    sa.UniqueConstraint('id_user', 'id_channel', name='_user_channel_uc')
    )
    op.create_table('media_tags',
    sa.Column('id_tag', sa.Integer(), nullable=False),
    sa.Column('id_media', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_media'], ['media_contents.id_media'], ),
    sa.ForeignKeyConstraint(['id_tag'], ['tags.id_tag'], ),
    sa.PrimaryKeyConstraint('id_tag', 'id_media')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('media_tags')
    op.drop_table('users_channels')
    op.drop_table('tags')
    op.drop_table('posts_media')
    op.drop_table('events')
    op.drop_table('posts')
    op.drop_table('media_contents')
    op.drop_table('channels')
    op.drop_table('auth_history')
    op.drop_table('users')
    op.drop_table('types_media')
    # ### end Alembic commands ###
