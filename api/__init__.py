from flask import Flask, g, jsonify
from flask_pyjwt import AuthManager
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flasgger import Swagger
from apispec import APISpec
from flask_apispec.extension import FlaskApiSpec
from apispec.ext.marshmallow import MarshmallowPlugin

from config import Config


app = Flask(__name__)
app.config.from_object(Config)
security_definitions = {
    "bearerAuth": {
                    "type": "apiKey",
                    "in": "header",
                    "name": "Authorization",
                    "bearerFormat": "JWT",
                    "description": "Enter: **'Bearer &lt;JWT&gt;'**, where JWT is the access token",
    }
}

app.config.update({
    'APISPEC_SPEC': APISpec(
        title='API MANAGE TLG',
        version='v1',
        plugins=[MarshmallowPlugin()],
        securityDefinitions=security_definitions,
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
swager = Swagger(app)
docs = FlaskApiSpec(app)
auth_manager = AuthManager(app)
auth_manager.init_app(app)

@app.errorhandler(422)
def validation_error(err):
    """Handles 422 errors"""
    messages = err.data.get('messages').get('json')
    return jsonify(messages)