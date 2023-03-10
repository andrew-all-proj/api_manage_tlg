from api import ma
from api.models.users_model import UserModel


class AuthSchema(ma.SQLAlchemySchema):
    class Meta:
        model = UserModel

    password = ma.Str(required=True)
    email = ma.Str(required=True)


class AutrResponseSchema(ma.SQLAlchemySchema):
    auth_token = ma.Str(required=True)
    id_user = ma.Int(required=True)
    user_name = ma.Str(required=True)
