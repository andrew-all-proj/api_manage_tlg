import datetime
from api import db
from api.models.media_contents_model import MediaContentModel
from api.models.mixins import ModelDbExt
from api.models.users_model import UserModel


class UsersToFeedbackBot(db.Model, ModelDbExt):
    __tablename__ = "users_to_feedback_bot"

    id_users_to_feedback_bot = db.Column(db.Integer, primary_key=True)
    id_feedback_bot = db.Column(db.Integer, db.ForeignKey("feedback_bots.id_feedback_bot"))
    id_user_telegram = db.Column(db.String(100), nullable=False)
    name_user = db.Column(db.String(100), nullable=False)
    data_update = db.Column(db.DateTime, nullable=False, onupdate=datetime.datetime.now, default=datetime.datetime.now)
    __table_args__ = (db.UniqueConstraint('id_user_telegram', 'id_feedback_bot', name='_user_bot_uc'),)

    def __init__(self, id_feedback_bot, id_user_telegram, name_user):
        self.id_feedback_bot = id_feedback_bot
        self.id_user_telegram = id_user_telegram
        self.name_user = name_user


class FeedbackBotsModel(db.Model, ModelDbExt):
    __tablename__ = "feedback_bots"

    id_feedback_bot = db.Column(db.Integer, primary_key=True)
    token_bot = db.Column(db.String(100), nullable=False, unique=True)
    name_bot = db.Column(db.String(100), nullable=False)
    id_admin_user = db.Column(db.Integer,  db.ForeignKey("users.id_user"), nullable=False)
    date_create = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    data_update = db.Column(db.DateTime, nullable=False, onupdate=datetime.datetime.now, default=datetime.datetime.now)
    is_archive = db.Column(db.Boolean, nullable=False, default=False)
    users_feedback = db.relationship(UsersToFeedbackBot, backref='users_to_feedback_bot', uselist=True, lazy='subquery')

    def __init__(self, id_admin_user, token_bot, name_bot):
        self.id_admin_user = id_admin_user
        self.token_bot = token_bot
        self.name_bot = name_bot


