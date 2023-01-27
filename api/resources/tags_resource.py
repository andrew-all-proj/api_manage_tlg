from flask_apispec.views import MethodResource
from flask_pyjwt import require_token, current_token

from api import g, db
from api.models.channels_model import ChannelModel, UserChannelModel
from api.models.media_contents_model import MediaContentModel
from api.models.media_tags_model import TagModel, tags
from flask_apispec import marshal_with, use_kwargs, doc
from sqlalchemy import and_
from webargs import fields

from api.sсhemas.media_contents_schema import MediaContentsSchema
from api.sсhemas.tag_schema import TagListSchema, TagSchema, TagCreateSchema, TagChangeSchema


def get_channel(id_channel, id_user):
    channel = ChannelModel.query.join(UserChannelModel, ChannelModel.id_channel == UserChannelModel.id_channel). \
        filter(and_(UserChannelModel.id_user == id_user,
                    ChannelModel.id_channel == id_channel),
               ChannelModel.is_archive == False).first()
    return channel


# /v1/tags
@doc(description='Api for tags', tags=['Tags'])
class TagsCreateResource(MethodResource):
    @require_token()
    @doc(security=[{"bearerAuth": []}])
    @doc(summary='Create new tag')
    @doc(description='Full: Create new tag')
    @marshal_with(TagSchema, code=201)
    @use_kwargs(TagCreateSchema, location='json')
    def post(self, **kwargs):
        channel = get_channel(kwargs.get("id_channel"), current_token.scope)
        if not channel:
            return {"error": "channel not found"}, 404
        tag = TagModel(**kwargs)
        if not tag.save():
            return {"error": "key is not uniq"}, 400
        return tag, 201


# /tags/channel/<int:id_channel>
@doc(description='Api for tags', tags=['Tags'])
class TagsListResource(MethodResource):
    @require_token()
    @doc(security=[{"bearerAuth": []}])
    @marshal_with(TagListSchema(many=True), code=200)
    @doc(summary='Get all tags by id channel')
    @doc(description='Full: Get all tags by id channel')
    def get(self, id_channel):
        channel = ChannelModel.query.join(UserChannelModel, ChannelModel.id_channel == UserChannelModel.id_channel). \
            filter(and_(UserChannelModel.id_user == current_token.scope,
                        ChannelModel.id_channel == id_channel,
                        ChannelModel.is_archive == False)).first()
        if not channel:
            return {"error": "channel not found"}, 404
        tags = TagModel.query.filter_by(id_channel=channel.id_channel).all()
        return tags, 200


# /tags/<int:id_tag>
@doc(description='Api for tags', tags=['Tags'])
class TagsResource(MethodResource):
    @require_token()
    @doc(security=[{"bearerAuth": []}])
    @marshal_with(TagListSchema, code=200)
    @doc(summary='Get tags by id tag')
    @doc(description='Full: Get tags by id tag')
    def get(self, id_tag):
        tag = TagModel.query.filter_by(id_tag=id_tag).first()
        if not tag:
            return {"error": "tag not found"}, 404
        channel = get_channel(tag.id_channel, current_token.scope)
        if not channel:
            return {"error": "tag not found"}, 404
        return tag, 200


    @require_token()
    @doc(security=[{"bearerAuth": []}])
    @doc(summary='Delete tags by id tag')
    @doc(description='Full: Delete tags by id tag')
    def delete(self, id_tag):
        tag = TagModel.query.filter_by(id_tag=id_tag).first()
        if not tag:
            return {"error": "tag not found"}, 404
        channel = get_channel(tag.id_channel, current_token.scope)
        if not channel:
            return {"error": "tag not found"}, 404
        tags_query = db.session.query(tags).filter_by(id_tag=id_tag)
        tags_query.delete()
        db.session.commit()
        if not tag.delete():
            return {"error": "tag delete"}, 404
        return {}, 200


    @require_token()
    @doc(security=[{"bearerAuth": []}])
    @marshal_with(TagListSchema, code=200)
    @use_kwargs(TagChangeSchema, location='json')
    @doc(summary='Update tag by id tag')
    @doc(description='Full: Update tags by id tag')
    def put(self, id_tag, **kwargs):
        tag = TagModel.query.filter_by(id_tag=id_tag).first()
        if not tag:
            return {"error": "tag not found"}, 404
        channel = get_channel(tag.id_channel, current_token.scope)
        if not channel:
            return {"error": "tag not found"}, 404
        tag.tag_name = kwargs.get('tag_name') or tag.tag_name
        if not tag.save():
            return {"error": "key is not uniq"}, 400
        return tag, 200


#/tags/<int:id_ tag>/settags
@doc(description='Api for tags', tags=['Tags'])
class MediaSetTagsResource(MethodResource):
    @require_token()
    @doc(security=[{"bearerAuth": []}])
    @use_kwargs({"tags": fields.List(fields.Int())}, location='json')
    @marshal_with(MediaContentsSchema, code=200)
    @doc(summary='Set tags to Media')
    @doc(description='Full: Set tags to Media')
    def put(self, id_media, **kwargs):
        media = MediaContentModel.query.filter(and_(MediaContentModel.id_user == current_token.scope,
                                                    MediaContentModel.id_media == id_media,
                                                    MediaContentModel.is_archive == False)).first()
        if not media:
            return {"error": "media not found"}, 404
        for id_tag in kwargs["tags"]:
            tag = TagModel.query.get(id_tag)
            if not tag:
                return {"error": f"tag {id_tag} not found"}, 404
            channel = get_channel(tag.id_channel, current_token.scope)
            if not channel:
                return {"error": f"channel {tag.id_channel} not found"}, 404
            media.tags.append(tag)
        if not media.save():
            return {"error": "save in bd"}, 400
        return media, 200


    @require_token()
    @doc(security=[{"bearerAuth": []}])
    @use_kwargs({"tags": fields.List(fields.Int())}, location='json')
    @marshal_with(MediaContentsSchema, code=200)
    @doc(summary='Unset tags to Media')
    @doc(description='Full: Unset tags to Media')
    def delete(self, id_media, **kwargs):
        media = MediaContentModel.query.filter(and_(MediaContentModel.id_user == current_token.scope,
                                                    MediaContentModel.id_media == id_media,
                                                    MediaContentModel.is_archive == False)).first()
        if not media:
            return {"error": "media not found"}, 404
        for id_tag in kwargs["tags"]:
            tag = TagModel.query.get(id_tag)
            if not tag:
                return {"error": f"tag {id_tag} not found"}, 404
            channel = get_channel(tag.id_channel, current_token.scope)
            if not channel:
                return {"error": f"channel not found"}, 404
            media.tags.remove(tag)
        if not media.save():
            return {"error": "save in bd"}, 400
        return media, 200
