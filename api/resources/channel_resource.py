from flask_apispec.views import MethodResource
from flask_pyjwt import require_token, current_token
from sqlalchemy import and_

from api.models.channels_model import ChannelModel, UserChannelModel
from api.sсhemas.channel_schema import ChannelSchema, ChannelRequestSchema, ChannelChangeSchema
from flask_apispec import marshal_with, use_kwargs, doc


def get_chanel(id_user, id_channel):
    return ChannelModel.query.join(UserChannelModel, ChannelModel.id_channel == UserChannelModel.id_channel). \
        filter(and_(UserChannelModel.id_user == id_user,
                    ChannelModel.id_channel == id_channel,
                    ChannelModel.is_archive == False)).first()


@doc(description='Api for channel', tags=['Channels'])
class ChannelsListResource(MethodResource):
    @require_token()
    @doc(security=[{"bearerAuth": []}])
    @marshal_with(ChannelSchema(many=True), code=200)
    @doc(summary='Get all channels')
    @doc(description='Full: Get all channel')
    def get(self):
        channels = ChannelModel.query.join(UserChannelModel, ChannelModel.id_channel == UserChannelModel.id_channel). \
            filter(and_(UserChannelModel.id_user == current_token.scope,
                        ChannelModel.is_archive == False)).all()
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
    @marshal_with(ChannelSchema(), code=200)
    @doc(summary='Get channel by id')
    @doc(description='Full: Get channel by id')
    def get(self, id_channel):
        channel = get_chanel(current_token.scope, id_channel)
        return channel, 200

    @require_token()
    @doc(security=[{"bearerAuth": []}])
    @marshal_with(ChannelSchema(), code=200)
    @doc(summary='Delete channel by id')
    @doc(description='Full: Delete channel by id')
    def delete(self, id_channel):
        channel = get_chanel(current_token.scope, id_channel)
        if not channel:
            return {"error": "channel not found"}, 404
        if channel.id_user_admin != current_token.scope:
            return {"error": "it can doing only admin"}, 400
        channel.to_archive()
        channel.save()
        return {}, 200

    @require_token()
    @doc(security=[{"bearerAuth": []}])
    @marshal_with(ChannelSchema, code=200)
    @use_kwargs(ChannelChangeSchema, location='json')
    @doc(description='Full: Change data chanel by id')
    @doc(summary='Change data chanel by id')
    def put(self, id_channel, **kwargs):
        channel = get_chanel(current_token.scope, id_channel)
        if not channel:
            return {"error": "channel not found"}, 404
        if channel.id_user_admin != current_token.scope:
            return {"error": "it can doing only admin"}, 400
        channel.name_channel = kwargs.get('name_channel') or channel.name_channel
        channel.link_channel = kwargs.get('link_channel') or channel.link_channel
        channel.id_telegram = kwargs.get('id_telegram') or channel.id_telegram
        if not channel.save():
            return {"error": "update data base"}, 400
        return channel, 200


@doc(description='Api for channel', tags=['Channels'])
class ChannelsSetUserResource(MethodResource):
    @require_token()
    @doc(security=[{"bearerAuth": []}])
    @marshal_with(ChannelSchema(), code=200)
    @doc(summary='Set channel for users')
    @doc(description='Full: Set channel for users')
    def put(self, id_channel, id_user):
        channel = get_chanel(current_token.scope, id_channel)
        if not channel:
            return {"error": "channel not found"}, 404
        user_channel = UserChannelModel(id_user=id_user, id_channel=id_channel)
        if not user_channel.save():
            return {"error": "update data base"}, 400
        return channel, 200


    @require_token()
    @doc(security=[{"bearerAuth": []}])
    @marshal_with(ChannelSchema(), code=200)
    @doc(summary='Unset channel for users')
    @doc(description='Full: Unset channel for users')
    def delete(self, id_channel, id_user):
        channel = get_chanel(current_token.scope, id_channel)
        if not channel:
            return {"error": "channel not found"}, 404
        if channel.id_user_admin != current_token.scope:
            return {"error": "it can doing only admin"}, 400
        user_channel = UserChannelModel.query.filter(and_(UserChannelModel.id_channel == id_channel,
                                                          UserChannelModel.id_user == id_user)).first()
        if not user_channel or not user_channel.delete():
            return {"error": "update data base"}, 400
        return {}, 200
