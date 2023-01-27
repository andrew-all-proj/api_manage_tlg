import datetime

from api import db
from api.models.media_contents_model import MediaContentModel
from api.models.mixins import ModelDbExt

media = db.Table('posts_media',
                db.Column('id_post', db.Integer, db.ForeignKey('posts.id_post'), primary_key=True),
                db.Column('id_media', db.Integer, db.ForeignKey('media_contents.id_media'), primary_key=True)
                )


class PostsModel(db.Model, ModelDbExt):
    __tablename__ = "posts"

    id_post = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(3000))
    id_user = db.Column(db.Integer, db.ForeignKey("users.id_user"), nullable=False)
    date_create = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    data_update = db.Column(db.DateTime, nullable=False, onupdate=datetime.datetime.now, default=datetime.datetime.now)
    is_archive = db.Column(db.Boolean, nullable=False, default=False)
    media = db.relationship(MediaContentModel, secondary=media, lazy='subquery')


    def __init__(self, id_user, text=None):
        self.text = text
        self.id_user = id_user

