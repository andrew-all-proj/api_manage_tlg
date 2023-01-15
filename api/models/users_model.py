import datetime
from passlib.apps import custom_app_context as pwd_context
from api import db, Config
from api.models.auth_model import AuthHistoryModel
from api.models.channels_model import UserChannelModel, ChannelModel
from api.models.media_contents_model import MediaContentModel
from api.models.mixins import ModelDbExt
from api.models.posts_model import PostsModel
from itsdangerous import URLSafeSerializer as Serialier
from itsdangerous import BadSignature, SignatureExpired


class UserModel(db.Model, ModelDbExt):
    __tablename__ = "users"

    id_user = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    id_telegram = db.Column(db.Integer, unique=True)
    email = db.Column(db.String(50), unique=True, nullable=False, default=False)
    password = db.Column(db.String(128), nullable=False)
    date_regestration = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    data_update = db.Column(db.DateTime, nullable=False, onupdate=datetime.datetime.now, default=datetime.datetime.now)
    role = db.Column(db.Boolean, nullable=False, default=False)
    is_archive = db.Column(db.Boolean, nullable=False, default=False)
    media = db.relationship(MediaContentModel)
    posts = db.relationship(PostsModel)
    user_channel = db.relationship(UserChannelModel)
    admin_channel = db.relationship(ChannelModel)
    auth = db.relationship(AuthHistoryModel)

    def __init__(self, email, password, name, id_telegram):
        self.name = name
        self.id_telegram = id_telegram
        self.email = email
        self.hash_password(password)

    def hash_password(self, password):
        self.password = pwd_context.hash(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password)

    def generate_auth_token(self, expiration=600):
        s = Serialier(Config.SECRET_KEY)
        return s.dumps({'id_user': self.id_user})
            

    @staticmethod
    def verify_auth_token(token):
        s = Serialier(Config.SECRET_KEY)
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None
        except BadSignature:
            return None
        user = UserModel.query.get(data['id_user'])
        return user




