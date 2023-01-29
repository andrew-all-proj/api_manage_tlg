from marshmallow import validate

from api import ma
from api.models.channels_model import ChannelModel


class ChannelSchema(ma.SQLAlchemySchema):
    class Meta:
        model = ChannelModel

    id_channel = ma.auto_field(required=True)
    name_channel = ma.auto_field()
    link_channel = ma.auto_field(required=True)
    id_telegram = ma.auto_field(required=True)
    is_archive = ma.auto_field(required=False)


class ChannelRequestSchema(ma.SQLAlchemySchema):
    class Meta:
        model = ChannelModel

    name_channel = ma.auto_field(required=True)
    link_channel = ma.auto_field(required=True)
    id_telegram = ma.auto_field(required=True)


class ChannelChangeSchema(ma.SQLAlchemySchema):
    class Meta:
        model = ChannelModel

    name_channel = ma.auto_field(required=False, validate=[validate.Length(min=3, max=36)])
    link_channel = ma.auto_field(required=False, validate=[validate.Length(min=5, max=36)])
    id_telegram = ma.auto_field(required=False, validate=[validate.Length(min=6, max=36)])
