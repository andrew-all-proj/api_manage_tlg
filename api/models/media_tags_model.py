from api import db
from api.models.mixins import ModelDbExt

tags = db.Table('media_tags',
                db.Column('id_tag', db.Integer, db.ForeignKey('tags.id_tag'), primary_key=True),
                db.Column('id_media', db.Integer, db.ForeignKey('media_contents.id_media'), primary_key=True)
                )

class TagModel(db.Model, ModelDbExt):
    __tablename__ = "tags"

    id_tag = db.Column(db.Integer, primary_key=True)
    tag_name = db.Column(db.String(50), nullable=False)
    id_channel = db.Column(db.Integer, db.ForeignKey("channels.id_channel"))
    __table_args__ = (db.UniqueConstraint('tag_name', 'id_channel', name='_tag_channel_uc'),)

    def __init__(self, tag_name, id_channel):
        self.tag_name = tag_name
        self.id_channel = id_channel



