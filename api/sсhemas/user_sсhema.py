from api import ma
from api.models.users_model import UserModel

#       schema        flask-restful
# object ------>  dict ----------> json

# Сериализация ответа(response)
class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = UserModel

    id_user = ma.auto_field(required=True)
    user_name = ma.auto_field(required=True)
    email = ma.Email(required=True)
    id_telegram = ma.auto_field(required=True)


# Десериализация запроса(request)
class UserRequestSchema(ma.SQLAlchemySchema):
    class Meta:
        model = UserModel

    user_name = ma.auto_field(required=True)
    password = ma.auto_field(required=True)
    email = ma.Email(required=True)
    id_telegram = ma.auto_field()


class UserLisrSchema(ma.SQLAlchemySchema):
    class Meta:
        model = UserModel

    id_user = ma.auto_field(required=True)
    user_name = ma.auto_field(required=True)


