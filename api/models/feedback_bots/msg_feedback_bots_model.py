import datetime
from api import db
from api.models.mixins import ModelDbExt


class MsgFeedbackBotsModel(db.Model, ModelDbExt):
    __tablename__ = "msg_feedback_bots"

    id_msg_feedback_bots = db.Column(db.Integer, primary_key=True)
    id_incoming_msg = db.Column(db.BigInteger, nullable=False)
    id_incoming_user = db.Column(db.BigInteger, nullable=False)
    id_incoming_chat = db.Column(db.BigInteger, nullable=False)
    id_feedback_bot = db.Column(db.Integer, db.ForeignKey("feedback_bots.id_feedback_bot"))
    date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)

    def __init__(self, id_incoming_msg, id_incoming_user, id_incoming_chat, id_feedback_bot):
        self.id_incoming_msg = id_incoming_msg
        self.id_incoming_user = id_incoming_user
        self.id_incoming_chat = id_incoming_chat
        self.id_feedback_bot = id_feedback_bot