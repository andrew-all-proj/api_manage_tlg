from marshmallow import validate

from api import ma
from api.models.users_model import UserModel


class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = UserModel

    id_user = ma.auto_field(required=True)
    user_name = ma.auto_field(required=True)
    email = ma.Email(required=True)
    id_telegram = ma.auto_field(required=True)


class UserRequestSchema(ma.SQLAlchemySchema):
    class Meta:
        model = UserModel

    user_name = ma.auto_field(required=False, validate=[validate.Length(min=3, max=36)])
    password = ma.auto_field(required=False, validate=[validate.Length(min=6, max=36)])
    email = ma.Email(required=False, validate=[validate.Length(min=3, max=36)])
    id_telegram = ma.auto_field(required=False, validate=[validate.Length(min=6, max=36)])


class UserLisrSchema(ma.SQLAlchemySchema):
    class Meta:
        model = UserModel

    id_user = ma.auto_field(required=True)
    user_name = ma.auto_field(required=True)
    is_archive = ma.auto_field(required=True)
