import datetime
from api import db


class AuthHistoryModel(db.Model):
    __tablename__ = "auth_history"

    id_auth_history = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey("users.id_user"), nullable=False)
    date_auth = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    from_is = db.Column(db.String(300), nullable=False)

