from flask_apispec.views import MethodResource
from flask_restful import reqparse
from api import db
from api.models.users_model import UserModel
from api.sсhemas.user_sсhema import UserSchema, UserRequestSchema, UserLisrSchema
from flask_apispec import  marshal_with, use_kwargs, doc
from flask_pyjwt import require_token, current_token

from helpers.shortscuts import get_object_or_404


@doc(description='Api for user.', tags=['Users'])
class UsersListResource(MethodResource):
    @require_token()
    @doc(security=[{"bearerAuth": []}])
    @marshal_with(UserLisrSchema(many=True), code=200)
    @doc(summary='Get all user delete after')
    @doc(description='Full: Get all User')
    def get(self):
        users = UserModel.query.all()
        return users, 200

    @doc(description='create new user')
    @marshal_with(UserSchema, code=201)
    @use_kwargs(UserRequestSchema, location='json')
    def post(self, **kwargs):
        user = UserModel.query.filter_by(email=kwargs["email"]).first()
        if user:
            return {"error": "email is exist"}, 400
        user = UserModel(**kwargs)
        db.session.add(user)
        db.session.commit()
        return user, 201

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
        user.user_to_archive()
        user.save()
        return {}, 200


    @require_token()
    @marshal_with(UserSchema, code=200)
    @use_kwargs(UserSchema, location='json')
    @doc(description='Full: Change data user with filters')
    @doc(summary='Change data user with filters')
    def put(self, user_id):
        user = UserModel.query.get(user_id)
        return user, 200



