from flask_apispec.views import MethodResource
from flask_pyjwt import require_token, current_token

from api import g
from api.models.channels_model import ChannelModel, UserChannelModel
from api.sсhemas.channel_schema import ChannelSchema, ChannelRequestSchema
from flask_apispec import marshal_with, use_kwargs, doc

from helpers.shortscuts import get_object_or_404


@doc(description='Api for channel', tags=['Channels'])
class ChannelsListResource(MethodResource):
    @require_token()
    @doc(security=[{"bearerAuth": []}])
    @marshal_with(ChannelSchema(many=True), code=200)
    @doc(summary='Get all channels')
    @doc(description='Full: Get all channel')
    def get(self):
        channels = ChannelModel.query.join(UserChannelModel, ChannelModel.id_channel == UserChannelModel.id_channel). \
            filter(UserChannelModel.id_user == current_token.scope).all()
        return channels, 200


    @require_token()
    @doc(security=[{"bearerAuth": []}])
    @doc(description='create new channel')
    @marshal_with(ChannelSchema, code=201)
    @use_kwargs(ChannelRequestSchema, location='json')
    def post(self, **kwargs):
        channel = ChannelModel.query.filter_by(id_telegram=kwargs["id_telegram"]).first()
        if channel:
            return {"error": "id_telegram is exist"}, 400
        channel = ChannelModel(id_user_admin=current_token.scope, **kwargs)
        channel.save()
        user_channel = UserChannelModel(channel.id_channel, current_token.scope)
        user_channel.save()
        return channel, 201



@doc(description='Api for channel', tags=['Channels'])
class ChannelsResource(MethodResource):
    @require_token()
    @doc(security=[{"bearerAuth": []}])
    @marshal_with(ChannelSchema(many=True), code=200)
    @doc(summary='Get all channels')
    @doc(description='Full: Get all channel')
    def get(self):
        channels = ChannelModel.query.join(UserChannelModel, ChannelModel.id_channel == UserChannelModel.id_channel). \
            filter(UserChannelModel.id_user == current_token.scope).all()
        return channels, 200