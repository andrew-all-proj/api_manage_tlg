from flask_apispec.views import MethodResource
from api.models.users_model import UserModel
from api.sсhemas.user_sсhema import UserSchema, UserRequestSchema, UserLisrSchema
from flask_apispec import marshal_with, use_kwargs, doc
from flask_pyjwt import require_token, current_token

from helpers.shortscuts import get_object_or_404


# /v1/users
@doc(description='Api for user.', tags=['Users'])
class UsersListResource(MethodResource):
    @require_token()
    @doc(security=[{"bearerAuth": []}])
    @marshal_with(UserLisrSchema(many=True), code=200)
    @doc(summary='Get all user')
    @doc(description='Full: Get all User')
    def get(self):
        users = UserModel.query.all()
        return users, 200

    @doc(description='create new user')
    @doc(summary='create new user')
    @marshal_with(UserSchema, code=201)
    @use_kwargs(UserRequestSchema, location='json')
    def post(self, **kwargs):
        user = UserModel.query.filter_by(email=kwargs["email"]).first()
        if user:
            return {"error": "email is exist"}, 400
        user = UserModel(**kwargs)
        if not user.save():
            return {"error": "update data base"}, 400
        return user, 201


# /v1/users/<user_id>
@doc(description='Api for user.', tags=['Users'])
class UserResource(MethodResource):
    @require_token()
    @doc(security=[{"bearerAuth": []}])
    @marshal_with(UserLisrSchema, code=200)
    @doc(description='Full: Get User by id')
    @doc(summary='Get User by id')
    def get(self, user_id):
        user = get_object_or_404(UserModel, user_id)
        if not user or user.is_archive:
            return {}, 200
        return user, 200

    @require_token()
    @doc(security=[{"bearerAuth": []}])
    @doc(description='Full: You can delete only own profile')
    @doc(summary='Delete User by id')
    def delete(self, user_id):
        user = get_object_or_404(UserModel, user_id)
        if not user:
            return {"error": "id user is not exist"}, 400
        if user.is_archive:
            return {"error": "user in archive"}, 400
        if user.id_user != current_token.scope:
            return {"error": "You can delete only own profile"}, 400
        user.to_archive()
        user.save()
        return {}, 200

    @require_token()
    @doc(security=[{"bearerAuth": []}])
    @marshal_with(UserSchema, code=200)
    @use_kwargs(UserRequestSchema, location='json')
    @doc(description='Full: Change data user by id')
    @doc(summary='Change data user by id')
    def put(self, user_id, **kwargs):
        user = UserModel.query.get(user_id)
        if not user:
            return {"error": "id user is not exist"}, 400
        if user.is_archive:
            return {"error": "user in archive"}, 400
        if user.id_user != current_token.scope:
            return {"error": "You can change only own profile"}, 400
        if kwargs.get('password') or kwargs.get('new_password'):
            if not user.verify_password(kwargs.get('password')):
                return {"error": "error password"}, 400
            user.password = user.hash_password(kwargs.get('new_password'))
        user.user_name = kwargs.get('user_name') or user.user_name
        user.id_telegram = kwargs.get('id_telegram') or user.id_telegram
        user.email = kwargs.get('email') or user.email
        if not user.save():
            return {"error": "update data base"}, 400
        return user, 200
