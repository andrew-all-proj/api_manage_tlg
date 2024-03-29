import datetime
from passlib.apps import custom_app_context as pwd_context
from api import db
from api.models.auth_model import AuthHistoryModel
from api.models.channels_model import UserChannelModel, ChannelModel
from api.models.media_contents_model import MediaContentModel
from api.models.mixins import ModelDbExt
from api.models.posts_model import PostsModel


class UserModel(db.Model, ModelDbExt):
    __tablename__ = "users"

    id_user = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(30), nullable=False)
    id_telegram = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(50), unique=True, nullable=False, default=False)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    password = db.Column(db.String(128), nullable=False)
    date_registration = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    data_update = db.Column(db.DateTime, nullable=False, onupdate=datetime.datetime.now, default=datetime.datetime.now)
    role = db.Column(db.String(30), nullable=False, default="user")
    is_archive = db.Column(db.Boolean, nullable=False, default=False)
    media = db.relationship(MediaContentModel)
    posts = db.relationship(PostsModel)
    user_channel = db.relationship(UserChannelModel)
    admin_channel = db.relationship(ChannelModel)
    auth = db.relationship(AuthHistoryModel)

    def __init__(self, email, password, user_name, id_telegram=None, is_archive=False):
        self.user_name = user_name
        self.id_telegram = self.id_split(id_telegram)
        self.email = email.lower()
        self.is_archive = is_archive
        self.password = self.hash_password(password)


    def hash_password(self, password):
        return pwd_context.hash(password)


    def verify_password(self, password):
        return pwd_context.verify(password, self.password)

    def confirmed_email(self, res):
        self.confirmed = res
