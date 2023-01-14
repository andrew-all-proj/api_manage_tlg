from api import Resource, g, auth
from flask_apispec.views import MethodResource
from api.sсhemas.user_sсhema import UserSchema, UserRequestSchema
from flask_apispec import  marshal_with, use_kwargs, doc


class TokenResource(MethodResource):
    @auth.login_required
    def get(self):
        token = g.user.generate_auth_token()
        return {'token': token} #.decode('ascii')