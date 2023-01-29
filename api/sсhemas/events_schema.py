from api import ma
from api.models.events_model import EventModel
from api.sсhemas.post_schema import PostSchema


class EventsSchema(ma.SQLAlchemySchema):
    class Meta:
        model = EventModel

    id_event = ma.auto_field(required=True)
    id_message = ma.auto_field(required=True)
    id_channel = ma.auto_field(required=True)
    date_start = ma.auto_field(required=True)
    date_stop = ma.auto_field(required=True)
    published = ma.auto_field(required=True)
    completed = ma.auto_field(required=True)
    post = ma.Nested(PostSchema)


class EventsCreateSchema(ma.SQLAlchemySchema):
    class Meta:
        model = EventModel

    id_post = ma.auto_field(required=True)
    id_channel = ma.auto_field(required=True)
    date_start = ma.auto_field(required=True)
    date_stop = ma.auto_field(required=False)


class EventsChangeSchema(ma.SQLAlchemySchema):
    class Meta:
        model = EventModel

    id_post = ma.auto_field(required=False)
    date_start = ma.auto_field(required=False)
    date_stop = ma.auto_field(required=False)
