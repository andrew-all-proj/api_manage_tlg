import datetime
from api import db
from api.models.media_tags_model import TagModel, tags
from api.models.mixins import ModelDbExt


class TypeMediaModel(db.Model, ModelDbExt):
    __tablename__ = "types_media"

    id_type_media = db.Column(db.Integer, primary_key=True)
    type_media = db.Column(db.String(20), nullable=False)
    name_dir = db.Column(db.String(250), nullable=False)
    extension = db.Column(db.String(20), nullable=False)


class MediaContentModel(db.Model, ModelDbExt):
    __tablename__ = "media_contents"

    id_media = db.Column(db.Integer, primary_key=True)
    id_type_media = db.Column(db.Integer, db.ForeignKey("types_media.id_type_media"), nullable=False)
    name_file = db.Column(db.String(250), nullable=False)
    description = db.Column(db.Text)
    date_download = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    last_time_used = db.Column(db.DateTime, nullable=False, onupdate=datetime.datetime.now,
                               default=datetime.datetime.now)
    id_user = db.Column(db.Integer, db.ForeignKey("users.id_user"), nullable=False)
    is_archive = db.Column(db.Boolean, nullable=False, default=False)
    type_media = db.relationship(TypeMediaModel, backref='types_media', uselist=False, lazy='joined')
    tags = db.relationship(TagModel, backref='tags', secondary=tags, uselist=True, lazy='subquery')


    def __init__(self, id_user, id_type_media, name_file, description=None):
        self.id_type_media = id_type_media
        self.name_file = name_file
        self.id_user = id_user
        self.description = description

class MediaModelAll:
    items = None
    total_count = None
