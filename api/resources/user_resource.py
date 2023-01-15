from flask_apispec.views import MethodResource
from flask_restful import reqparse
from api import db, app, auth, g, Config
from api.models.users_model import UserModel
from api.sсhemas.user_sсhema import UserSchema, UserRequestSchema
from flask_apispec import  marshal_with, use_kwargs, doc



@doc(description='Api for user.', tags=['Users'])
class UsersListResource(MethodResource):
    @auth.login_required
    @doc(security=[{"basicAuth": []}])
    @marshal_with(UserSchema(many=True), code=200)
    @doc(summary='Get all user delete after')
    @doc(description='Full: Get all User')
    def get(self):
        #print(g.user.name)
        users = UserModel.query.all()
        return users, 200

    @doc(description='create new user')
    @marshal_with(UserSchema, code=201)
    @use_kwargs(UserRequestSchema, location='json')
    def post(self, **kwargs):
        user = UserModel(**kwargs)
        db.session.add(user)
        db.session.commit()
        if not user.id_user:
            return f"User with username:{user.name} already exist", 400
        return user, 201

@doc(description='Api for user.', tags=['Users'])
class UserResource(MethodResource):
    @auth.login_required
    @marshal_with(UserSchema, code=200)
    @doc(description='Full: Get User by id')
    @doc(summary='Get User by id')
    def get(self, user_id):
        user = UserModel.query.get(user_id)
        return user, 200


