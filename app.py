import logging

from api import api, app, docs
#from api.resources.auth_resource import TokenResource
from api.resources.auth_resource import TokenResource, ConfirmEmail, SendTokenConfirmEmail
from api.resources.channel_resource import ChannelsListResource, ChannelsResource, ChannelsSetUserResource
from api.resources.events_resource import EventsListResource, EventsResource, EventsCreateResource
from api.resources.feedback_bots_resource import FeedBackBotResource, FeedBackBotsListResource
from api.resources.media_contents_resource import MediaListResource, MediaResource, MediaDownloadResource
from api.resources.posts_resource import PostsListResource, AddMediaToPostResource, PostsResource, PostsCreateResource
from api.resources.tags_resource import TagsListResource, MediaSetTagsResource, TagsResource, TagsCreateResource, \
    TagsMediaIdResource
from api.resources.users_to_feedback_resource import FeedBackBotsUsersListResource, FeedBackBotsUserResource
from config import Config
from api.resources.user_resource import UsersListResource, UserResource

# CRUD

# Create --> POST
# Read --> GET
# Update --> PUT
# Delete --> DELETE
api.add_resource(TokenResource,
                 f'/{Config.VERSION}/auth')  # POST
api.add_resource(SendTokenConfirmEmail,
                 f'/{Config.VERSION}/email/<int:id_user>')  # GET
api.add_resource(ConfirmEmail,
                 f'/{Config.VERSION}/email/confirm/<token>')

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
                 f'/{Config.VERSION}/media')  # GET/filter, POST
api.add_resource(MediaResource,
                 f'/{Config.VERSION}/media/<int:id_media>')  # GET PUT
api.add_resource(MediaDownloadResource,
                 f'/{Config.VERSION}/media/download/<int:id_media>') # GET

api.add_resource(PostsListResource,
                 f'/{Config.VERSION}/posts/')  # GET, POST
api.add_resource(PostsCreateResource,
                 f'/{Config.VERSION}/posts')
api.add_resource(PostsResource,
                 f'/{Config.VERSION}/posts/<int:id_post>')  # GET
api.add_resource(AddMediaToPostResource,
                 f'/{Config.VERSION}/posts/<int:id_post>/setmedia')  # PUT DELETE

api.add_resource(EventsListResource,
                 f'/{Config.VERSION}/events/channels/<int:id_channel>')  # GET
api.add_resource(EventsCreateResource,
                 f'/{Config.VERSION}/events')  # POST
api.add_resource(EventsResource,
                 f'/{Config.VERSION}/events/<int:id_event>')  # GET

api.add_resource(TagsListResource,
                 f'/{Config.VERSION}/tags/channel/<int:id_channel>')  # GET
api.add_resource(MediaSetTagsResource,
                 f'/{Config.VERSION}/media/<int:id_media>/settags')  # PUT DELETE
api.add_resource(TagsCreateResource,
                 f'/{Config.VERSION}/tags')  # POST
api.add_resource(TagsResource,
                 f'/{Config.VERSION}/tags/<int:id_tag>')  # GET PUT DELETE
api.add_resource(TagsMediaIdResource,
                 f'/{Config.VERSION}/tags/media/<int:id_media>')  # GET PUT DELETE

api.add_resource(FeedBackBotsListResource,
                 f'/{Config.VERSION}/feedback_bots')  # GET(ALL) POST
api.add_resource(FeedBackBotResource,
                 f'/{Config.VERSION}/feedback_bots/<int:id_feedback_bot>')  # GET PUT DELETE

api.add_resource(FeedBackBotsUsersListResource,
                 f'/{Config.VERSION}/feedback_bots/users')  # GET(ALL) POST
api.add_resource(FeedBackBotsUserResource,
                 f'/{Config.VERSION}/feedback_bots/users/<int:id_users_to_feedback_bot>')  # GET PUT DELETE


docs.register(TokenResource)
docs.register(SendTokenConfirmEmail)
docs.register(ConfirmEmail)

docs.register(UserResource)
docs.register(UsersListResource)

docs.register(ChannelsListResource)
docs.register(ChannelsResource)
docs.register(ChannelsSetUserResource)

docs.register(MediaListResource)
docs.register(MediaResource)
docs.register(MediaDownloadResource)

docs.register(PostsListResource)
docs.register(PostsCreateResource)
docs.register(PostsResource)
docs.register(AddMediaToPostResource)

docs.register(EventsListResource)
docs.register(EventsCreateResource)
docs.register(EventsResource)

docs.register(TagsListResource)
docs.register(TagsResource)
docs.register(MediaSetTagsResource)
docs.register(TagsCreateResource)
docs.register(TagsMediaIdResource)

docs.register(FeedBackBotsListResource)
docs.register(FeedBackBotResource)

docs.register(FeedBackBotsUsersListResource)
docs.register(FeedBackBotsUserResource)

logging.info("Start app")
if __name__ == '__main__':
    app.run(debug=Config.DEBUG, port=Config.PORT)
