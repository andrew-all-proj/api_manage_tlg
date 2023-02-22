from flask import request, url_for
from api import auth_manager
from flask_apispec.views import MethodResource
from flask_apispec import doc, use_kwargs, marshal_with
from api.models.auth_model import AuthHistoryModel
from api.models.users_model import UserModel
from api.sсhemas.auth_schema import AuthSchema, AutrResponseSchema


#/v1/auth
from service.confirm_email import generate_confirmation_token, confirm_token
from service.send_email import send_email


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
        if not user.confirmed:
            return {"error": "Your email is not verified"}, 401
        if user.verify_password(password):
            auth_token = auth_manager.auth_token(email, user.id_user)
            auth_history = AuthHistoryModel(id_user=user.id_user, from_is=request.headers["Host"])
            auth_history.save()
            #refresh_token = auth_manager.refresh_token(user.id_user)  # добавить функцию!!!!
            return {f"auth_token": auth_token.signed}, 200
        return {"error": "Invalid login or password"}, 401


#/email/<int:id user>
@doc(description='Api for confirmation email', tags=['Authentication'])
class SendTokenConfirmEmail(MethodResource):
    @doc(summary='GET id user')
    @doc(description='Send email with link for confirmation it')
    @marshal_with(AutrResponseSchema, code=200)
    def get(self, id_user):
        user = UserModel.query.filter_by(id_user=id_user).first()
        if not user:
            return {"error": "Invalid id user"}, 401
        token = generate_confirmation_token(user.email)
        confirm_url = url_for('confirmemail', token=token, _external=True)
        send_email(
              recipients=['andrew.publik.mail@gmail.com']
            , subject=f"confirm email"
            , body=f"link confirm email: {confirm_url}"
        )
        return 200


#/email/<str:token>
@doc(description='Api for get token confirm email', tags=['Authentication'])
class ConfirmEmail(MethodResource):
    @doc(summary='GET token with email')
    @doc(description='GET token with email')
    @marshal_with(AutrResponseSchema, code=200)
    def get(self, token):
        result = confirm_token(token)
        if not result:
            return {"error": "token burned"}, 401
        user = UserModel.query.filter_by(email=result).first()
        if not user:
            return {"error": "Invalid email"}, 401
        user.confirmed_email(True)
        user.save()
        return 200


