from flask_apispec.views import MethodResource
from flask_pyjwt import require_token, current_token
from sqlalchemy import and_
from webargs import fields

from api.models.media_contents_model import MediaContentModel
from api.models.posts_model import PostsModel, PostsModelAll
from flask_apispec import marshal_with, doc, use_kwargs
from api.sсhemas.post_schema import PostSchema, PostCreateSchema, PostSchemaAll


def get_post(id_user, id_post):
    return PostsModel.query.filter(and_(PostsModel.id_user == id_user,
                                        PostsModel.id_post == id_post,
                                        PostsModel.is_archive == False)).first()



# /posts/?filters
@doc(description='Api for posts', tags=['Posts'])
class PostsListResource(MethodResource):
    @require_token()
    @doc(security=[{"bearerAuth": []}])
    @marshal_with(PostSchemaAll, code=200)
    @use_kwargs({
        "page": fields.Int(),
        "per_page": fields.Int()}, location="query")
    @doc(summary='Get all posts')
    @doc(description='Full: Get all posts')
    def get(self, **kwargs):
        page = 1
        per_page = 100
        if kwargs.get("per_page"):
            per_page = kwargs["per_page"]
        if kwargs.get("page"):
            page = kwargs["page"]

        post_model = PostsModelAll
        posts = PostsModel.query.filter(and_(PostsModel.id_user == current_token.scope,
                                             PostsModel.is_archive == False))
        count = posts.count()
        post_model.total_count = count
        posts = posts.paginate(page=page, per_page=per_page, error_out=False).items
        post_model.items = posts

        return post_model, 200


# /v1/posts
@doc(description='Api for posts', tags=['Posts'])
class PostsCreateResource(MethodResource):
    @require_token()
    @doc(security=[{"bearerAuth": []}])
    @marshal_with(PostSchema, code=201)
    @use_kwargs(PostCreateSchema, location='json')
    @doc(summary='Create new post')
    @doc(description='Full: Create new post')
    def post(self, **kwargs):
        posts = PostsModel(id_user=current_token.scope, **kwargs)
        if not posts.save():
            return {"error": "save in bd"}, 404
        return posts, 201


# posts/<int:id_post>
@doc(description='Api for posts', tags=['Posts'])
class PostsResource(MethodResource):
    @require_token()
    @doc(security=[{"bearerAuth": []}])
    @marshal_with(PostSchema, code=200)
    @doc(summary='Get post by id')
    @doc(description='Full: Get post by id')
    def get(self, id_post):
        return get_post(current_token.scope, id_post), 200

    @require_token()
    @doc(security=[{"bearerAuth": []}])
    @marshal_with(PostSchema, code=200)
    @use_kwargs(PostCreateSchema, location='json')
    @doc(summary='Change post by id')
    @doc(description='Full: Change post by id')
    def put(self, id_post, **kwargs):
        post = get_post(current_token.scope, id_post)
        if not post:
            return {"error": "post not found"}, 404
        post.text = kwargs.get('text') or post.text
        if not post.save():
            return {"error": "update data base"}, 400
        return post, 200

    @require_token()
    @doc(security=[{"bearerAuth": []}])
    @marshal_with(PostSchema, code=200)
    @doc(summary='Delete post by id')
    @doc(description='Full: Delete post by id')
    def delete(self, id_post):
        post = get_post(current_token.scope, id_post)
        if not post:
            return {"error": "channel not found"}, 404
        post.to_archive()
        if not post.save():
            return {"error": "update data base"}, 400
        return {}, 200


# posts/<int:id_post>/setmedia
@doc(description='Api for posts', tags=['Posts'])
class AddMediaToPostResource(MethodResource):
    @require_token()
    @doc(security=[{"bearerAuth": []}])
    @marshal_with(PostSchema, code=200)
    @use_kwargs({"media": fields.List(fields.Int())}, location='json')
    @doc(summary='Add media to post')
    @doc(description='Add media to post')
    def put(self, id_post, **kwargs):
        post = get_post(current_token.scope, id_post)
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

    @require_token()
    @doc(security=[{"bearerAuth": []}])
    @marshal_with(PostSchema, code=200)
    @use_kwargs({"media": fields.List(fields.Int())}, location='json')
    @doc(summary='Unset media from post')
    @doc(description='Unset media from post')
    def delete(self, id_post, **kwargs):
        post = get_post(current_token.scope, id_post)
        if not post:
            return {"error": "post not found"}, 404
        if not kwargs.get("media"):
            return {"error": "error key media"}, 404
        for id_media in kwargs["media"]:
            media = MediaContentModel.query.get(id_media)
            if not media:
                return {"error": f"id media {id_media} not found"}, 404
            post.media.remove(media)
        if not post.save():
            return {"error": "save in bd"}, 400
        return post, 200
