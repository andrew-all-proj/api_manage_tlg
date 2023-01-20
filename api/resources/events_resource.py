from flask_apispec.views import MethodResource
from api import g, db
from api.models.channels_model import ChannelModel
from api.models.events_model import EventModel
from api.sсhemas.events_schema import EventsSchema, EventsRequestSchema
from flask_apispec import marshal_with, use_kwargs, doc
from sqlalchemy import and_


@doc(description='Api for events', tags=['Events'])
class EventsListResource(MethodResource):
    #@auth.login_required
    @doc(security=[{"basicAuth": []}])
    @marshal_with(EventsSchema(many=True), code=200)
    @doc(summary='Get all events')
    @doc(description='Full: Get all events')
    def get(self, id_channel):
        channel = ChannelModel.query.filter(and_(ChannelModel.id_channel == id_channel,
                                                 ChannelModel.id_user_admin == g.user.id_user)).first()
        if not channel:
            return f"error chanel", 400
        events = EventModel.query.filter(EventModel.id_channel == id_channel).all()
        return events, 200

@doc(description='Api for events', tags=['Events'])
class EventsResource(MethodResource):
    #@auth.login_required
    @doc(description='create new events')
    @marshal_with(EventsRequestSchema, code=201)
    @use_kwargs(EventsSchema, location='json')
    @doc(security=[{"basicAuth": []}])
    def post(self, **kwargs):
        event = EventModel(**kwargs)
        event.save()
        return event, 201
