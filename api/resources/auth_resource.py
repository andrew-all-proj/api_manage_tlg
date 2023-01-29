from flask import request
from api import auth_manager
from flask_apispec.views import MethodResource
from flask_apispec import doc, use_kwargs, marshal_with
from api.models.auth_model import AuthHistoryModel
from api.models.users_model import UserModel
from api.sсhemas.auth_schema import AuthSchema, AutrResponseSchema


#/v1/auth
@doc(description='Api for authentication user', tags=['Authentication'])
class TokenResource(MethodResource):
    @doc(summary='Get token')
    @doc(description='Get token')
    @use_kwargs(AuthSchema, location='json')
    @marshal_with(AutrResponseSchema, code=200)
    def post(self, email, password):
        user = UserModel.query.filter_by(email=email).first()
        if not user:
            return {"error": "Invalid login or password"}, 401
        if user.verify_password(password):
            auth_token = auth_manager.auth_token(email, user.id_user)
            auth_history = AuthHistoryModel(id_user=user.id_user, from_is=request.headers["Host"])
            auth_history.save()
            #refresh_token = auth_manager.refresh_token(user.id_user)  # добавить функцию!!!!
            return {f"auth_token": auth_token.signed}, 200
        return {"error": "Invalid login or password"}, 401

