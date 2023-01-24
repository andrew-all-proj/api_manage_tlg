from datetime import datetime
import os

import werkzeug
from flask import request, jsonify
from flask_apispec.views import MethodResource
from flask_pyjwt import require_token, current_token
from flask_restful import reqparse
from webargs import fields
from werkzeug.utils import secure_filename

from api import g, app
from api.models.media_contents_model import TypeMediaModel, MediaContentModel
from api.sсhemas.media_contents_schema import MediaContentsSchema, MediaContentsRequestSchema, MediaContentsPostSchema
from flask_apispec import marshal_with, use_kwargs, doc

from config import Config


@doc(description='Api for media', tags=['Media'])
class MediaListResource(MethodResource):
    @require_token()
    @doc(security=[{"bearerAuth": []}])
    @marshal_with(MediaContentsSchema(many=True), code=200)
    @use_kwargs({"page": fields.Int(), "per_page": fields.Int()}, location="query")
    @doc(summary='Get all media')
    @doc(description='Full: Get all media')
    def get(self, **kwargs):
        page = 1
        per_page = 3
        if kwargs.get("page"):
            page = kwargs["page"]
        if kwargs.get("per_page"):
            per_page = kwargs["per_page"]
        media = MediaContentModel.query.filter(MediaContentModel.id_user == current_token.scope).paginate(page, per_page, error_out=False).items
        return media, 200


    @require_token()
    @doc(security=[{"bearerAuth": []}])
    @doc(description='create new media')
    @marshal_with(MediaContentsSchema, code=201)
    @use_kwargs({'file': fields.Raw()}, location='files')
    def post(self, **kwarg):
        file = kwarg.get('file')
        if not file:
            return {"error": "Not file"}, 400
        print(file)
        type_media = TypeMediaModel.query.filter_by(extension=file.content_type.split("/")[1]).first()
        if not type_media:
            return {"error": str(file.content_type.split("/")[1])}, 400
        suffix_name = datetime.now().strftime("%y%m%d_%H%M%S")
        gen_name = f"{type_media.type_media}_{suffix_name}.{type_media.extension}"
        try:
            file.save(f"{Config.BASE_DIR}/{current_token.scope}/{type_media.name_dir}/{gen_name}")  # file/1/images/12333.jpg
        except FileNotFoundError:
            os.makedirs(f"{Config.BASE_DIR}/{current_token.scope}/{type_media.name_dir}")
            file.save(f"{Config.BASE_DIR}/{current_token.scope}/{type_media.name_dir}/{gen_name}")
        except Exception:
            return {"error": "error save"}, 400
        media = MediaContentModel(id_type_media=type_media.id_type_media, name_file=gen_name,  id_user=current_token.scope)
        if not media.save():
            os.remove(f"{Config.BASE_DIR}/{current_token.scope}/{type_media.name_dir}/{gen_name}")
            return {"error": "error save"}, 400
        return media, 201
