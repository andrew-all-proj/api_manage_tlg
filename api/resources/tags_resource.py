from flask_apispec.views import MethodResource
from api import auth, g, db
from api.models.media_contents_model import MediaContentModel
from api.models.media_tags_model import TagModel
from flask_apispec import marshal_with, use_kwargs, doc
from sqlalchemy import and_
from webargs import fields

from api.sсhemas.media_contents_schema import MediaContentsSchema
from api.sсhemas.tag_schema import TagListSchema, TagSchema


@doc(description='Api for tags', tags=['Tags'])
class TagsListResource(MethodResource):
    @auth.login_required
    @doc(security=[{"basicAuth": []}])
    @marshal_with(TagListSchema(many=True), code=200)
    @doc(summary='Get all tags')
    @doc(description='Full: Get all tags')
    def get(self):
        tags = TagModel.query.all()
        return tags, 200


    @auth.login_required
    @doc(description='create new tag')
    @marshal_with(TagSchema, code=201)
    @use_kwargs(TagListSchema, location='json')
    @doc(security=[{"basicAuth": []}])
    def post(self, **kwargs):
        tag = TagModel(**kwargs)
        tag.save()
        return tag, 201


@doc(description='Api for tags', tags=['Tags'])
class MediaSetTagsResource(MethodResource):
    @auth.login_required
    @doc(security=[{"basicAuth": []}])
    @use_kwargs({"tags": fields.List(fields.Int())}, location='json')
    @marshal_with(MediaContentsSchema, code=200)
    @doc(summary='Set tags to Media')
    @doc(description='Full: Set tags to Media')
    def put(self, id_media, **kwargs):
        media = MediaContentModel.query.get(id_media)
        if not media:
            return f"error media id: {id_media}", 404
        for id_tag in kwargs["tags"]:
            tag = TagModel.query.get(id_tag)
            media.tags.append(tag)
        media.save()

        return media, 200