from api import api, app, docs
from api.resources.auth_resource import TokenResource
from api.resources.channel_resource import ChannelsListResource
from config import Config
from api.resources.user_resource import UsersListResource, UserResource

# CRUD

# Create --> POST
# Read --> GET
# Update --> PUT
# Delete --> DELETE
api.add_resource(TokenResource,
                 f'/{Config.VERSION}/auth/token')  # GET
api.add_resource(UsersListResource,
                 f'/{Config.VERSION}/users')  # GET, POST
api.add_resource(UserResource,
                 f'/{Config.VERSION}/users/<int:user_id>')  # GET, POST
api.add_resource(ChannelsListResource,
                 f'/{Config.VERSION}/channels')  # GET, POST

docs.register(TokenResource)
docs.register(UserResource)
docs.register(UsersListResource)
docs.register(ChannelsListResource)
if __name__ == '__main__':
    app.run(debug=Config.DEBUG, port=Config.PORT)
