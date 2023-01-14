from api import ma
from api.models.users_model import UserModel

#       schema        flask-restful
# object ------>  dict ----------> json

# Сериализация ответа(response)
class ChannelSchema(ma.SQLAlchemySchema):
    class Meta:
        model = UserModel
        fields = ('id_channel', 'name_channel', "link_channel", "id_telegram")
        #exclude = ['id_user', 'name'] исключить


# Десериализация запроса(request)
class ChannelRequestSchema(ma.SQLAlchemySchema):
    class Meta:
        model = UserModel

    name_channel = ma.Str(required=True)
    link_channel = ma.Str(required=True)
    id_telegram = ma.Str(required=True)