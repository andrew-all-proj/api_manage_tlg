from api import api, app, docs
from api.resources.auth import TokenResource
from config import Config
from api.resources.user_resource import UsersListResource, UserResource

# CRUD

# Create --> POST
# Read --> GET
# Update --> PUT
# Delete --> DELETE
api.add_resource(UsersListResource,
                 f'/{Config.VERSION}/users')  # GET, POST
api.add_resource(UserResource,
                 f'/{Config.VERSION}/users/<int:user_id>')  # GET, POST

api.add_resource(TokenResource,
                 f'/{Config.VERSION}/auth/token')  # GET, POST

docs.register(UserResource)
docs.register(UsersListResource)
if __name__ == '__main__':
    app.run(debug=Config.DEBUG, port=Config.PORT)
