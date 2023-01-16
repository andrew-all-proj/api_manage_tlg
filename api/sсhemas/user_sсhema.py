from api import ma
from api.models.users_model import UserModel

#       schema        flask-restful
# object ------>  dict ----------> json

# Сериализация ответа(response)
class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = UserModel
        fields = ('id_user', 'user_name', "email", "id_telegram")
        #exclude = ['id_user', 'name'] исключить


# Десериализация запроса(request)
class UserRequestSchema(ma.SQLAlchemySchema):
    class Meta:
        model = UserModel

    user_name = ma.Str(required=True)
    password = ma.Str(required=True)
    email = ma.Str(required=True)
    id_telegram = ma.Int(required=True)


