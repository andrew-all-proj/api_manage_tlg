from api import db
from api.models.events_model import EventModel


class PostsMediaModel(db.Model):
    __tablename__ = "posts_media"
    id_post_media = db.Column(db.Integer, primary_key=True)
    id_post = db.Column(db.Integer, db.ForeignKey("posts.id_post"), nullable=False)
    id_media = db.Column(db.Integer, db.ForeignKey("media_contents.id_media"), nullable=False)


class PostsModel(db.Model):
    __tablename__ = "posts"

    id_post = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(3000))
    id_user = db.Column(db.Integer, db.ForeignKey("users.id_user"), nullable=False)
    id_post_media = db.Column(db.Integer, nullable=False)
    media = db.relationship(PostsMediaModel)
    event = db.relationship(EventModel)