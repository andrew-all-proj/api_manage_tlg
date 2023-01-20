import datetime
from api import db
from api.models.mixins import ModelDbExt


class AuthHistoryModel(db.Model, ModelDbExt):
    __tablename__ = "auth_history"

    id_auth_history = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey("users.id_user"), nullable=False)
    date_auth = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    from_is = db.Column(db.String(300), nullable=False)

    def __init__(self, id_user, from_is):
        self.id_user = id_user
        self.from_is = from_is
