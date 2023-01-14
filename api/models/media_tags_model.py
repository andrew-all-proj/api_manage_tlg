from api import db

class MediaTagModel(db.Model):
    __tablename__ = "media_tags"
    id_media_tags = db.Column(db.Integer, primary_key=True)
    id_tag = db.Column(db.Integer, db.ForeignKey("tags.id_tag"), nullable=False)
    id_media = db.Column(db.Integer, db.ForeignKey("media_contents.id_media"), nullable=False)



class TagModel(db.Model):
    __tablename__ = "tags"

    id_tag = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    id_channel = db.Column(db.Integer, db.ForeignKey("channels.id_channel"))
    tags = db.relationship(MediaTagModel)