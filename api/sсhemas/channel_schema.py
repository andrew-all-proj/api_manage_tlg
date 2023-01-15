from api import ma
from api.models.channels_model import ChannelModel, UserChannelModel


#       schema        flask-restful
# object ------>  dict ----------> json

# Сериализация ответа(response)
class ChannelSchema(ma.SQLAlchemySchema):
    class Meta:
        model = ChannelModel

    id_channel = ma.auto_field(required=True)
    name_channel = ma.auto_field()
    link_channel = ma.auto_field(required=True)
    id_telegram = ma.auto_field(required=True)


# Десериализация запроса(request)
class ChannelRequestSchema(ma.SQLAlchemySchema):
    class Meta:
        model = ChannelModel

    name_channel = ma.Str(required=True)
    link_channel = ma.Str(required=True)
    id_telegram = ma.Str(required=True)