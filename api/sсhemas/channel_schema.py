from api import ma
from api.models.users_model import UserModel

#       schema        flask-restful
# object ------>  dict ----------> json

# Сериализация ответа(response)
class ChanelSchema(ma.SQLAlchemySchema):
    class Meta:
        model = UserModel
        fields = ('id_chanel', 'name_chanel', "link_chanel", "id_telegram")
        #exclude = ['id_user', 'name'] исключить


# Десериализация запроса(request)
class ChanelRequestSchema(ma.SQLAlchemySchema):
    class Meta:
        model = UserModel

    name_chanel = ma.Str(required=True)
    link_chanel = ma.Str(required=True)
    id_telegram = ma.Str(required=True)