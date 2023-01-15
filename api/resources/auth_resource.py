from api import Resource, g, auth
from flask_apispec.views import MethodResource
from flask_apispec import doc

@doc(description='Api for authentication user', tags=['Authentication'])
class TokenResource(MethodResource):
    @auth.login_required
    @doc(summary='Get token')
    @doc(description='Get token')
    def get(self):
        token = g.user.generate_auth_token()
        return {'token': token} #.decode('ascii')