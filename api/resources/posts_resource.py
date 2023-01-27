from flask_apispec.views import MethodResource
from flask_pyjwt import require_token, current_token
from sqlalchemy import and_
from webargs import fields

from api.models.media_contents_model import MediaContentModel
from api.models.posts_model import PostsModel
from flask_apispec import marshal_with, doc, use_kwargs
from api.sсhemas.post_schema import PostSchema, PostCreatetSchema
from api.sсhemas.user_sсhema import UserSchema


@doc(description='Api for posts', tags=['Posts'])
class PostsListResource(MethodResource):
    @require_token()
    @doc(security=[{"bearerAuth": []}])
    @marshal_with(PostSchema(many=True), code=200)
    @doc(summary='Get all posts')
    @doc(description='Full: Get all posts')
    def get(self):
        posts = PostsModel.query.filter(and_(PostsModel.id_user == current_token.scope,
                                             PostsModel.is_archive == False)).all()
        return posts, 200

    @require_token()
    @doc(security=[{"bearerAuth": []}])
    @marshal_with(PostSchema, code=201)
    @use_kwargs(PostCreatetSchema, location='json')
    @doc(summary='Create new post')
    @doc(description='Full: Create new post')
    def post(self, **kwargs):
        posts = PostsModel(id_user=current_token.scope, **kwargs)
        if not posts.save():
            return {"error": "save in bd"}, 404
        return posts, 201


@doc(description='Api for posts', tags=['Posts'])
class PostsResource(MethodResource):
    @require_token()
    @doc(security=[{"bearerAuth": []}])
    @marshal_with(PostSchema, code=200)
    @doc(summary='Get post by id')
    @doc(description='Full: Get post by id')
    def get(self, id_post):
        posts = PostsModel.query.filter(and_(PostsModel.id_user == current_token.scope,
                                             PostsModel.id_post == id_post,
                                             PostsModel.is_archive == False)).first()
        return posts, 200


@doc(description='Api for posts', tags=['Posts'])
class AddMediaToPostResource(MethodResource):
    @require_token()
    @doc(security=[{"bearerAuth": []}])
    @marshal_with(PostSchema, code=200)
    @use_kwargs({"media": fields.List(fields.Int())}, location='json')
    @doc(summary='Add media to post')
    @doc(description='Add media to post')
    def put(self, id_post, **kwargs):
        post = PostsModel.query.filter(and_(PostsModel.id_user == current_token.scope,
                                            PostsModel.id_post == id_post,
                                            PostsModel.is_archive == False)).first()
        if not post:
            return {"error": "post not found"}, 404
        for id_media in kwargs["media"]:
            media = MediaContentModel.query.get(id_media)
            if not media:
                return {"error": f"id media {id_media} not found"}, 404
            post.media.append(media)
        if not post.save():
            return {"error": "save in bd"}, 400
        return post, 200
