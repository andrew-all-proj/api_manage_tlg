import datetime
from api import db
from api.models.events_model import EventModel
from api.models.media_tags_model import TagModel
from api.models.mixins import ModelDbExt


class UserChannelModel(db.Model, ModelDbExt):
    __tablename__ = "users_channels"
    id_user_channel = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey("users.id_user"), nullable=False)
    id_channel = db.Column(db.Integer, db.ForeignKey("channels.id_channel"), nullable=False)
    __table_args__ = (db.UniqueConstraint('id_user', 'id_channel', name='_user_channel_uc'),
                      )

    def __init__(self, id_channel, id_user):
        self.id_channel = id_channel
        self.id_user = id_user



class ChannelModel(db.Model, ModelDbExt):
    __tablename__ = "channels"

    id_channel = db.Column(db.Integer, primary_key=True)
    name_channel = db.Column(db.String(200), nullable=False)
    link_channel = db.Column(db.String(200), nullable=False)
    id_telegram = db.Column(db.String(200), nullable=False, unique=True)
    date_create = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    data_update = db.Column(db.DateTime, nullable=False, onupdate=datetime.datetime.now, default=datetime.datetime.now)
    is_archive = db.Column(db.Boolean, nullable=False, default=False)
    id_user_admin = db.Column(db.Integer, db.ForeignKey("users.id_user"), nullable=False)
    users_channels = db.relationship(UserChannelModel)
    tags = db.relationship(TagModel)
    event = db.relationship(EventModel)

    def __init__(self, id_user_admin, name_channel, link_channel, id_telegram):
        self.name_channel = name_channel
        self.link_channel = link_channel
        self.id_telegram = id_telegram
        self.id_user_admin = id_user_admin

    def channel_to_archive(self):
        self.is_archive = True


