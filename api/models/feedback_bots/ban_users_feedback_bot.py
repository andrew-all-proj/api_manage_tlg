import datetime
from api import db
from api.models.mixins import ModelDbExt


class BanUsersFeedbackBotModel(db.Model, ModelDbExt):
    __tablename__ = "ban_users_feedback_bot"

    id_ban_users_feedback_bot = db.Column(db.Integer, primary_key=True)
    id_user_telegram = db.Column(db.BigInteger, nullable=False)
    id_feedback_bot = db.Column(db.Integer, db.ForeignKey("feedback_bots.id_feedback_bot"))
    date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)

    def __init__(self, id_user_telegram, id_feedback_bot):
        self.id_user_telegram = id_user_telegram
        self.id_feedback_bot = id_feedback_bot
