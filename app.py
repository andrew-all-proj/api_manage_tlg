from api import api, app, docs
from api.resources.auth_resource import TokenResource
from api.resources.channel_resource import ChannelsListResource
from api.resources.events_resource import EventsListResource, EventsResource
from api.resources.media_contents_resource import MediaListResource
from api.resources.posts_resource import PostsListResource, AddMediaToPostResource
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
api.add_resource(MediaListResource,
                 f'/{Config.VERSION}/media')  # GET, POST
api.add_resource(PostsListResource,
                 f'/{Config.VERSION}/posts')  # GET, POST
api.add_resource(AddMediaToPostResource,
                 f'/{Config.VERSION}/posts/<int:id_post>')  # GET, POST
api.add_resource(EventsListResource,
                 f'/{Config.VERSION}/events/<int:id_channel>')  # GET
api.add_resource(EventsResource,
                 f'/{Config.VERSION}/events')  # POST

docs.register(TokenResource)
docs.register(UserResource)
docs.register(UsersListResource)
docs.register(ChannelsListResource)
docs.register(MediaListResource)
docs.register(PostsListResource)
docs.register(AddMediaToPostResource)
docs.register(EventsListResource)
docs.register(EventsResource)

if __name__ == '__main__':
    app.run(debug=Config.DEBUG, port=Config.PORT)
