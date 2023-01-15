from api import ma
from api.models.events_model import EventModel
from api.sсhemas.tag_schema import TagSchema
from api.sсhemas.type_media_schema import TypeMediaSchema

#       schema        flask-restful
# object ------>  dict ----------> json

# Сериализация ответа(response)



class EventsSchema(ma.SQLAlchemySchema):
    class Meta:
        model = EventModel

    id_post = ma.auto_field(required=True)
    id_message = ma.auto_field(required=True)
    id_channel = ma.auto_field(required=True)
    date_start = ma.auto_field(required=True)
    date_stop = ma.auto_field(required=True)


class EventsRequestSchema(ma.SQLAlchemySchema):
    class Meta:
        model = EventModel

    id_post = ma.auto_field(required=True)
    id_event = ma.auto_field(required=True)
    id_message = ma.auto_field(required=True)
    id_channel = ma.auto_field(required=True)
    date_start = ma.auto_field(required=True)
    date_stop = ma.auto_field(required=True)
    completed = ma.auto_field(required=True)