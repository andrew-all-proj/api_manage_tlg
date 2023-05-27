import logging
import os
from datetime import datetime
import random

from flask import send_file
from flask_apispec import marshal_with, use_kwargs, doc
from flask_apispec.views import MethodResource
from flask_pyjwt import require_token, current_token
from sqlalchemy import and_
from sqlalchemy.orm import aliased
from webargs import fields

from api import db
from api.models.media_contents_model import TypeMediaModel, MediaContentModel, MediaModelAll
from api.models.media_tags_model import TagModel, tags
from api.models.posts_model import PostsModel, media as PostsMediaModel
from api.sсhemas.media_contents_schema import MediaContentsSchema, MediaChangeSchema, MediaSchemaAll
from config import CONTENT_DIR


def get_media(id_user, id_media):
    return MediaContentModel.query.filter(and_(MediaContentModel.id_user == id_user,
                                               MediaContentModel.id_media == id_media,
                                               MediaContentModel.is_archive == False)).first()


# /v1/media/
@doc(description='Api for media', tags=['Media'])
class MediaListResource(MethodResource):
    @require_token()
    @doc(security=[{"bearerAuth": []}])
    @marshal_with(MediaSchemaAll, code=200)
    @use_kwargs({"page": fields.Int(),
                 "per_page": fields.Int(),
                 "is_archive": fields.Boolean(),
                 "last_time_used": fields.DateTime(),
                 "published": fields.Boolean(),
                 "id_channel": fields.Int(),
                 "limit": fields.Int(),
                 "list_tags": fields.Str()}, location="query")
    @doc(summary='Get all media')
    @doc(description='Full: Get all media')
    def get(self, **kwargs):
        page = 1
        per_page = 3
        is_arhive = False
        limit = 1000
        if kwargs.get("page"):
            page = kwargs["page"]
        if kwargs.get("per_page"):
            per_page = kwargs["per_page"]
        if kwargs.get("is_archive"):
            is_arhive = kwargs["is_archive"]
        media_model = MediaModelAll
        if kwargs.get("limit"):
            limit = kwargs["limit"]
        media = MediaContentModel.query.filter(and_(MediaContentModel.id_user == current_token.scope,
                                                    MediaContentModel.is_archive == is_arhive))
        if kwargs.get("last_time_used"):
            last_time_used = kwargs["last_time_used"]
            media = media.filter(MediaContentModel.last_time_used < last_time_used)
        if kwargs.get("published"):
            media_not_used = db.session.query(MediaContentModel.id_media). \
                outerjoin(PostsMediaModel, MediaContentModel.id_media == PostsMediaModel.c.id_media). \
                outerjoin(PostsModel, PostsMediaModel.c.id_post == PostsModel.id_post). \
                filter(MediaContentModel.id_user == current_token.scope). \
                filter(PostsMediaModel.c.id_media.is_(None)). \
                distinct()
            media = media.filter(MediaContentModel.id_media.in_(media_not_used))
        if kwargs.get("list_tags"):
            list_tags = [int(num) for num in kwargs["list_tags"].split(",")]
            query_list_in_tags = db.session.query(MediaContentModel.id_media) \
                .join(tags, MediaContentModel.id_media == tags.c.id_media) \
                .join(TagModel, TagModel.id_tag == tags.c.id_tag) \
                .filter(TagModel.id_tag.in_(list_tags))
            media = media.filter(MediaContentModel.id_media.in_(query_list_in_tags))
        subq = media.limit(limit).subquery()
        ua = aliased(MediaContentModel, subq)  # Make subquery bcs don't work limit
        media_model.total_count = 100
        media = db.session.query(ua)
        media_model.total_count = media.count()
        media_model.items = media.paginate(page=page, per_page=per_page, error_out=False).items
        return media_model, 200

    @require_token()
    @doc(security=[{"bearerAuth": []}])
    @doc(description='Full: create new media')
    @doc(summary='Create new media')
    @marshal_with(MediaContentsSchema, code=201)
    @use_kwargs({'file': fields.Raw()}, location='files')
    def post(self, **kwarg):
        logging.info(f"UPLOAD MEDIA")
        print("LOAD MIDIA")
        file = kwarg.get('file')
        if not file:
            return {"error": "Not file"}, 400
        root, ext = os.path.splitext(file.filename)
        type_media = TypeMediaModel.query.filter_by(extension=ext.lstrip('.').lower()).first()
        if not type_media:
            logging.info(f'error type media: {str(file.content_type.split("/")[1])}')
            return {"error": str(file.content_type.split("/")[1])}, 400
        if (type_media.type_media == 'audio'):
            gen_name = f"{root}.{type_media.extension}"
        else:
            random_number = str(random.randint(1, 100))
            suffix_name = datetime.now().strftime("%y%m%d_%H%M%S%f") + random_number
            gen_name = f"{type_media.type_media}_{suffix_name}.{type_media.extension}"
        try:
            print(f"{CONTENT_DIR}/{current_token.scope}/{type_media.name_dir}/{gen_name}")
            file.save(
                f"{CONTENT_DIR}/{current_token.scope}/{type_media.name_dir}/{gen_name}")  # file/1/images/12333.jpg
        except FileNotFoundError:
            os.makedirs(f"{CONTENT_DIR}/{current_token.scope}/{type_media.name_dir}")  # create dir
            file.save(f"{CONTENT_DIR}/{current_token.scope}/{type_media.name_dir}/{gen_name}")
        except:
            return {"error": "error save"}, 400
        media = MediaContentModel(id_type_media=type_media.id_type_media, name_file=gen_name,
                                  id_user=current_token.scope)
        if not media.save():
            os.remove(f"{CONTENT_DIR}/{current_token.scope}/{type_media.name_dir}/{gen_name}")
            logging.info(f'error save media')
            return {"error": "error save"}, 400
        return media, 201


# /v1/media/<id_media>
@doc(description='Api for media', tags=['Media'])
class MediaResource(MethodResource):
    @require_token()
    @doc(security=[{"bearerAuth": []}])
    @marshal_with(MediaContentsSchema, code=200)
    @doc(summary='Get media by id')
    @doc(description='Full: Get media by id')
    def get(self, id_media):
        media = get_media(current_token.scope, id_media)
        return media, 200

    @require_token()
    @doc(security=[{"bearerAuth": []}])
    @marshal_with(MediaContentsSchema, code=200)
    @doc(summary='Delete media by id')
    @doc(description='Full: Delete media by id')
    def delete(self, id_media):
        media = get_media(current_token.scope, id_media)
        if not media:
            return {"error": "media not found"}, 404
        media.to_archive()
        media.save()
        return {}, 200

    @require_token()
    @doc(security=[{"bearerAuth": []}])
    @marshal_with(MediaContentsSchema, code=200)
    @use_kwargs(MediaChangeSchema, location='json')
    @doc(description='Full: Change data chanel by id')
    @doc(summary='Change data chanel by id')
    def put(self, id_media, **kwargs):
        media = get_media(current_token.scope, id_media)
        if not media:
            return {"error": "media not found"}, 404
        media.description = kwargs.get('description') or media.description
        if not media.save():
            return {"error": "update data base"}, 400
        return media, 200


# /v1/media/download/<id_media>
@doc(description='Api for media', tags=['Media'])
class MediaDownloadResource(MethodResource):
    # @require_token()
    # @doc(security=[{"bearerAuth": []}])
    @doc(summary='Download media by id')
    @doc(description='Full: Download media by id')
    def get(self, id_media):
        media = MediaContentModel.query.filter(and_(MediaContentModel.id_media == id_media,
                                                    MediaContentModel.is_archive == False)).first()
        if not media:
            return {"error": "Not file"}, 404
        type_media = TypeMediaModel.query.filter_by(id_type_media=media.id_type_media).first()
        if not os.path.exists(f"{CONTENT_DIR}/{media.id_user}/{type_media.name_dir}/{media.name_file}"):
            return {"error": "Not file"}, 404
        return send_file(
            path_or_file=f"{CONTENT_DIR}/{media.id_user}/{type_media.name_dir}/{media.name_file}",
            mimetype="application/octet-stream",
            as_attachment=False,
        )
