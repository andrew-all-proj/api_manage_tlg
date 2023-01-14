import datetime
from api import db


class EventModel(db.Model):
    __tablename__ = "events"

    id_event = db.Column(db.Integer, primary_key=True)
    id_post = db.Column(db.Integer, db.ForeignKey("posts.id_post"), nullable=False)
    id_message = db.Column(db.Integer, nullable=False, default=0)
    id_channel = db.Column(db.Integer, db.ForeignKey("channels.id_channel"), nullable=False)
    date_start = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    date_stop = db.Column(db.DateTime)
    completed = db.Column(db.Boolean, nullable=False, default=False)