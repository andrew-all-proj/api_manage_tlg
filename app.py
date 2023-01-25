from api import api, app, docs
#from api.resources.auth_resource import TokenResource
from api.resources.auth_resource import TokenResource
from api.resources.channel_resource import ChannelsListResource, ChannelsResource, ChannelsSetUserResource
from api.resources.events_resource import EventsListResource, EventsResource
from api.resources.media_contents_resource import MediaListResource, MediaResource, MediaDownloadResource
from api.resources.posts_resource import PostsListResource, AddMediaToPostResource
from api.resources.tags_resource import TagsListResource, MediaSetTagsResource
from config import Config
from api.resources.user_resource import UsersListResource, UserResource

# CRUD

# Create --> POST
# Read --> GET
# Update --> PUT
# Delete --> DELETE
api.add_resource(TokenResource,
                 f'/{Config.VERSION}/auth')  # POST

api.add_resource(UsersListResource,
                 f'/{Config.VERSION}/users')  # GET, POST
api.add_resource(UserResource,
                 f'/{Config.VERSION}/users/<int:user_id>')  # GET, DELETE, PUT

api.add_resource(ChannelsListResource,
                 f'/{Config.VERSION}/channels')  # GET, POST
api.add_resource(ChannelsResource,
                 f'/{Config.VERSION}/channels/<int:id_channel>')  # GET, DELETE, PUT
api.add_resource(ChannelsSetUserResource,
                 f'/{Config.VERSION}/channels/<int:id_channel>/users/<int:id_user>')  # DELETE, PUT

api.add_resource(MediaListResource,
                 f'/{Config.VERSION}/media/')  # GET/filter, POST
api.add_resource(MediaResource,
                 f'/{Config.VERSION}/media/<int:id_media>')  # GET
api.add_resource(MediaDownloadResource,
                 f'/{Config.VERSION}/media/download/<int:id_media>') # GET

api.add_resource(PostsListResource,
                 f'/{Config.VERSION}/posts/')  # GET, POST

api.add_resource(AddMediaToPostResource,
                 f'/{Config.VERSION}/posts/<int:id_post>')  # GET, POST
api.add_resource(EventsListResource,
                 f'/{Config.VERSION}/events/<int:id_channel>')  # GET
api.add_resource(EventsResource,
                 f'/{Config.VERSION}/events')  # POST
api.add_resource(TagsListResource,
                 f'/{Config.VERSION}/tags')  # POST
api.add_resource(MediaSetTagsResource,
                 f'/{Config.VERSION}/media/<int:id_media>/set_tags')  # POST

docs.register(TokenResource)
docs.register(UserResource)
docs.register(UsersListResource)

docs.register(ChannelsListResource)
docs.register(ChannelsResource)
docs.register(ChannelsSetUserResource)

docs.register(MediaListResource)
docs.register(MediaResource)
docs.register(MediaDownloadResource)

docs.register(PostsListResource)
docs.register(AddMediaToPostResource)
docs.register(EventsListResource)
docs.register(EventsResource)
docs.register(TagsListResource)
docs.register(MediaSetTagsResource)

if __name__ == '__main__':
    app.run(debug=Config.DEBUG, port=Config.PORT)
