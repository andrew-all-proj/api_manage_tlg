from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_httpauth import HTTPBasicAuth
from flasgger import Swagger
from apispec import APISpec
from flask_apispec.extension import FlaskApiSpec
from apispec.ext.marshmallow import MarshmallowPlugin
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
app.config.update({
    'APISPEC_SPEC': APISpec(
        title='Notes Project',
        version='v1',
        plugins=[MarshmallowPlugin()],
        #securityDefinitions=security_definitions,
        security=[],
        openapi_version='2.0.0'
    ),
    'APISPEC_SWAGGER_URL': '/swagger',  # URI API Doc JSON
    'APISPEC_SWAGGER_UI_URL': '/swagger-ui'  # URI UI of API Doc
})

api = Api(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)
auth = HTTPBasicAuth()
#swager = Swagger(app)
docs = FlaskApiSpec(app)

@auth.verify_password
def verify_password(name, username_or_token):
    from api.models.users_model import UserModel
    user = UserModel.verify_auth_token(username_or_token)
    if not user:
        user = UserModel.query.filter_by(name=name).first()
        if not user or not user.verify_password(username_or_token):
            return False
    g.user = user
    return True
