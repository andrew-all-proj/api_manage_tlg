from flask_apispec.views import MethodResource
from api import auth, g
from api.models.channels_model import ChannelModel, UserChannelModel
from api.sсhemas.channel_schema import ChannelSchema, ChannelRequestSchema
from flask_apispec import marshal_with, use_kwargs, doc


@doc(description='Api for channel', tags=['Channels'])
class ChannelsListResource(MethodResource):
    @auth.login_required
    @doc(security=[{"basicAuth": []}])
    @marshal_with(ChannelSchema(many=True), code=200)
    @doc(summary='Get all channels')
    @doc(description='Full: Get all channel')
    def get(self):
        channels = ChannelModel.query.join(UserChannelModel, ChannelModel.id_channel == UserChannelModel.id_channel). \
            filter_by(id_user=g.user.id_user).all()
        return channels, 200

    @doc(description='create new channel')
    @marshal_with(ChannelSchema, code=201)
    @use_kwargs(ChannelRequestSchema, location='json')
    @auth.login_required
    @doc(security=[{"basicAuth": []}])
    def post(self, **kwargs):
        channel = ChannelModel(id_user_admin=g.user.id_user, **kwargs)
        channel.save()
        user_channel = UserChannelModel(channel.id_channel, g.user.id_user)
        user_channel.save()
        if not channel.id_channel:
            return f"Channel is :{channel.name_channel} already exist", 400
        return channel, 201
