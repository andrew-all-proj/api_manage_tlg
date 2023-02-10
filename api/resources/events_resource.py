from flask_apispec.views import MethodResource
from flask_pyjwt import require_token, current_token
from webargs import fields

from api.models.channels_model import UserChannelModel
from api.models.events_model import EventModel
from api.models.posts_model import PostsModel, PostsModelAll
from api.resources.channel_resource import get_chanel
from api.resources.posts_resource import get_post
from api.sсhemas.events_schema import EventsSchema, EventsCreateSchema, EventsChangeSchema, EventSchemaAll
from flask_apispec import marshal_with, use_kwargs, doc
from sqlalchemy import and_


# /events/channels/<int:id_channel>
@doc(description='Api for events', tags=['Events'])
class EventsListResource(MethodResource):
    @require_token()
    @doc(security=[{"bearerAuth": []}])
    @marshal_with(EventSchemaAll, code=200)
    @use_kwargs({
        "date_start": fields.DateTime(),
        "date_stop": fields.DateTime(),
        "page": fields.Int(),
        "per_page": fields.Int(),
        "completed": fields.Boolean()}, location="query")
    @doc(summary='Get all events and sort filters')
    @doc(description='Full: Get all events and sort filters')
    def get(self, id_channel, **kwargs):

        page = 1
        per_page = 100
        date_start = '2000-01-01 13:00:00.00'
        date_stop = '2050-01-01 13:00:00.00'
        completed = False

        channel = get_chanel(current_token.scope, id_channel)
        if not channel:
            return {"error": "Not channel"}, 404
        if kwargs.get("per_page"):
            per_page = kwargs["per_page"]
        if kwargs.get("page"):
            page = kwargs["page"]
        if kwargs.get("date_start"):
            date_start = kwargs["date_start"]
        if kwargs.get("date_stop"):
            date_stop = kwargs["date_stop"]
        if kwargs.get("completed"):
            completed = kwargs["completed"]
        events_model = PostsModelAll
        events = EventModel.query.filter(and_(EventModel.id_channel == id_channel,
                                              EventModel.date_start > date_start,
                                              EventModel.date_start < date_stop,
                                              EventModel.completed == completed))
        events_model.total_count = events.count()
        events_model.items = events.paginate(page, per_page, error_out=False).items

        return events_model, 200


# /events/<int:id_event>
@doc(description='Api for events', tags=['Events'])
class EventsResource(MethodResource):
    @require_token()
    @doc(security=[{"bearerAuth": []}])
    @doc(description='Full: Get event by id')
    @doc(summary='Get event by id')
    @marshal_with(EventsSchema, code=200)
    def get(self, id_event):
        event = EventModel.query.get(id_event)
        if not event:
            return {"error": "Not event"}, 404
        channel = get_chanel(current_token.scope, event.id_channel)
        if not channel:
            return {"error": "Not event"}, 404
        return event, 200

    @require_token()
    @doc(security=[{"bearerAuth": []}])
    @doc(description='Full: Change events by id')
    @doc(summary='Change events by id')
    @marshal_with(EventsSchema, code=200)
    @use_kwargs(EventsChangeSchema, location='json')
    def put(self, id_event, **kwargs):
        event = EventModel.query.get(id_event)
        if not event:
            return {"error": "Not event"}, 404
        channel = get_chanel(current_token.scope, event.id_channel)
        if not channel:
            return {"error": "Not event"}, 404
        event.date_start = kwargs.get('date_start') or event.date_start
        event.date_stop = kwargs.get('date_stop') or event.date_stop
        if kwargs.get('id_post'):  # check belongs to post users channels
            list_users = UserChannelModel.query.filter_by(id_channel=channel.id_channel).all()
            for user in list_users:
                post = PostsModel.query.filter(and_(PostsModel.id_user == user.id_user,
                                                    PostsModel.id_post == kwargs["id_post"])).first()
                if post:
                    event.id_post = kwargs["id_post"]
        if not event.save():
            return {"error": "update data base"}, 400
        return event, 200

    @require_token()
    @doc(security=[{"bearerAuth": []}])
    @doc(description='create new events')
    @doc(summary='Change events by id')
    @marshal_with(EventsSchema, code=200)
    def delete(self, id_event):
        event = EventModel.query.filter(and_(EventModel.id_event == id_event, EventModel.completed == False)).first()
        if not event:
            return {"error": "Not event"}, 404
        channel = get_chanel(current_token.scope, event.id_channel)
        if not channel:
            return {"error": "Not event"}, 404
        list_users = UserChannelModel.query.filter(and_(UserChannelModel.id_channel == channel.id_channel,
                                                        UserChannelModel.id_user == current_token.scope)).all()
        if not list_users:
            return {"error": "Not event"}, 404
        event.completed = True
        if not event.save():
            return {"error": "update data base"}, 404
        return event, 200


# /events
@doc(description='Api for events', tags=['Events'])
class EventsCreateResource(MethodResource):
    @require_token()
    @doc(security=[{"bearerAuth": []}])
    @doc(description='Full: create new events')
    @doc(summary='create new events')
    @marshal_with(EventsSchema, code=201)
    @use_kwargs(EventsCreateSchema, location='json')
    def post(self, **kwargs):
        channel = get_chanel(current_token.scope, kwargs.get('id_channel'))
        if not channel:
            return {"error": "Not channel"}, 404
        post = get_post(current_token.scope, kwargs.get('id_post'))
        if not post:
            return {"error": "Not post"}, 404
        event = EventModel(**kwargs)
        if not event.save():
            return {"error": "save in bd"}, 400
        return event, 201
