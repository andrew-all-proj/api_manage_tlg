import logging
from datetime import datetime
import os

from flask import send_file
from flask_apispec.views import MethodResource
from flask_pyjwt import require_token, current_token
from sqlalchemy import and_
from webargs import fields
from flask_apispec import marshal_with, use_kwargs, doc

from api.models.media_contents_model import TypeMediaModel, MediaContentModel, MediaModelAll
from api.sсhemas.media_contents_schema import MediaContentsSchema, MediaChangeSchema, MediaSchemaAll

from config import Config, CONTENT_DIR


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
    @use_kwargs({"page": fields.Int(), "per_page": fields.Int(),
                 "is_archive": fields.Boolean(), "last_time_used": fields.DateTime()}, location="query")
    @doc(summary='Get all media')
    @doc(description='Full: Get all media')
    def get(self, **kwargs):
        page = 1
        per_page = 3
        is_arhive = False
        if kwargs.get("page"):
            page = kwargs["page"]
        if kwargs.get("per_page"):
            per_page = kwargs["per_page"]
        if kwargs.get("is_archive"):
            is_arhive = kwargs["is_archive"]
        media_model = MediaModelAll
        media = MediaContentModel.query.filter(and_(MediaContentModel.id_user == current_token.scope,
                                                    MediaContentModel.is_archive == is_arhive))
        if kwargs.get("last_time_used"):
            last_time_used = kwargs["last_time_used"]
            media = media.filter(MediaContentModel.last_time_used < last_time_used)
        count = media.count()
        media_model.total_count = count
        media = media.paginate(page=page, per_page=per_page, error_out=False).items
        media_model.items = media
        return media_model, 200

    @require_token()
    @doc(security=[{"bearerAuth": []}])
    @doc(description='Full: create new media')
    @doc(summary='Create new media')
    @marshal_with(MediaContentsSchema, code=201)
    @use_kwargs({'file': fields.Raw()}, location='files')
    def post(self, **kwarg):
        logging.info(f"UPLOAD MEDIA")
        file = kwarg.get('file')
        if not file:
            return {"error": "Not file"}, 400
        root, ext = os.path.splitext(file.filename)
        type_media = TypeMediaModel.query.filter_by(extension=ext.lstrip('.').lower()).first()
        if not type_media:
            logging.info(f'error type media: {str(file.content_type.split("/")[1])}')
            return {"error": str(file.content_type.split("/")[1])}, 400
        suffix_name = datetime.now().strftime("%y%m%d_%H%M%S")
        gen_name = f"{type_media.type_media}_{suffix_name}.{type_media.extension}"
        try:
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
    #@require_token()
    #@doc(security=[{"bearerAuth": []}])
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
