from flask_apispec.views import MethodResource
from api import g
from api.models.posts_model import PostsModel
from flask_apispec import marshal_with, doc
from api.sсhemas.post_schema import PostSchema
from api.sсhemas.user_sсhema import UserSchema


@doc(description='Api for posts', tags=['Posts'])
class PostsListResource(MethodResource):
    #@auth.login_required
    @doc(security=[{"basicAuth": []}])
    @marshal_with(PostSchema(many=True), code=200)
    @doc(summary='Get all posts')
    @doc(description='Full: Get all posts')
    def get(self):
        posts = PostsModel.query.filter(PostsModel.id_user == g.user.id_user).all()
        return posts, 200


@doc(description='Api for posts', tags=['Posts'])
class AddMediaToPostResource(MethodResource):
    #@auth.login_required
    @doc(security=[{"basicAuth": []}])
    @marshal_with(UserSchema(), code=200)
    @doc(summary='Add media to post')
    @doc(description='Add media to post')
    def put(self, **kwargs):
        #post = PostsModel(id_user=g.user.id_user, **kwargs)
        #post.save()
        return "post", 201

