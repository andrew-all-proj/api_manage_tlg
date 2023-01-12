import datetime
from api import db
from api.models.events_model import EventModel
from api.models.media_tags_model import TagModel


class UserChanelModel(db.Model):
    __tablename__ = "users_chanels"
    id_user_chanel = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey("users.id_user"), nullable=False)
    id_chanel = db.Column(db.Integer, db.ForeignKey("chanels.id_chanel"), nullable=False)



class ChanelModel(db.Model):
    __tablename__ = "chanels"

    id_chanel = db.Column(db.Integer, primary_key=True)
    name_chanel = db.Column(db.String(200), nullable=False)
    link_chanel = db.Column(db.String(200), nullable=False)
    id_telegram = db.Column(db.String(200), nullable=False)
    date_create = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    data_update = db.Column(db.DateTime, nullable=False, onupdate=datetime.datetime.now, default=datetime.datetime.now)
    id_user_admin = db.Column(db.Integer, db.ForeignKey("users.id_user"), nullable=False)
    users_chanels = db.relationship(UserChanelModel)
    tags = db.relationship(TagModel)
    event = db.relationship(EventModel)