import datetime
from api import db
from api.models.events_model import EventModel
from api.models.media_tags_model import TagModel


class UserChanelModel(db.Model):
    __tablename__ = "users_chanels"
    id_user_chanel = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey("users.id_user"), nullable=False)
    id_chanel = db.Column(db.Integer, db.ForeignKey("chanels.id_chanel"), nullable=False)

    def __init__(self, id_chanel, id_user):
        self.id_chanel = id_chanel
        self.id_user = id_user

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except:
            db.session.rollback()



class ChanelModel(db.Model):
    __tablename__ = "chanels"

    id_chanel = db.Column(db.Integer, primary_key=True)
    name_chanel = db.Column(db.String(200), nullable=False)
    link_chanel = db.Column(db.String(200), nullable=False)
    id_telegram = db.Column(db.String(200), nullable=False, unique=True)
    date_create = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    data_update = db.Column(db.DateTime, nullable=False, onupdate=datetime.datetime.now, default=datetime.datetime.now)
    id_user_admin = db.Column(db.Integer, db.ForeignKey("users.id_user"), nullable=False)
    users_chanels = db.relationship(UserChanelModel)
    tags = db.relationship(TagModel)
    event = db.relationship(EventModel)

    def __init__(self, id_user_admin, name_chanel, link_chanel, id_telegram):
        self.name_chanel = name_chanel
        self.link_chanel = link_chanel
        self.id_telegram = id_telegram
        self.id_user_admin = id_user_admin


    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except:
            db.session.rollback()