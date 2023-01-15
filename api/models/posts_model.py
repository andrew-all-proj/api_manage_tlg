from api import db
from api.models.events_model import EventModel
from api.models.media_contents_model import MediaContentModel


media = db.Table('posts_media',
                db.Column('id_post', db.Integer, db.ForeignKey('posts.id_post'), primary_key=True),
                db.Column('id_media', db.Integer, db.ForeignKey('media_contents.id_media'), primary_key=True)
                )


class PostsModel(db.Model):
    __tablename__ = "posts"

    id_post = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(3000))
    id_user = db.Column(db.Integer, db.ForeignKey("users.id_user"), nullable=False)
    media = db.relationship(MediaContentModel, secondary=media, lazy='subquery')
    event = db.relationship(EventModel)

    def __init__(self, id_user, text=None):
        self.text = text
        self.id_user = id_user


    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except:
            db.session.rollback()
