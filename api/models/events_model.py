import datetime
from api import db
from api.models.mixins import ModelDbExt
from api.models.posts_model import PostsModel


class EventModel(db.Model, ModelDbExt):
    __tablename__ = "events"

    id_event = db.Column(db.Integer, primary_key=True)
    id_post = db.Column(db.Integer, db.ForeignKey("posts.id_post"), nullable=False)
    id_message = db.Column(db.Integer, nullable=False, default=0)
    id_channel = db.Column(db.Integer, db.ForeignKey("channels.id_channel"), nullable=False)
    date_start = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    date_stop = db.Column(db.DateTime)
    completed = db.Column(db.Boolean, nullable=False, default=False)
    post = db.relationship(PostsModel, backref='posts', uselist=False, lazy='subquery')

    def __init__(self, id_post, id_channel, date_start, date_stop=None, id_message=0):
        self.id_post = id_post
        self.id_channel = id_channel
        self.date_start = date_start
        self.date_stop = date_stop
        self.id_message = id_message
