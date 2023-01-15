import os
from flask_apispec.views import MethodResource
from api import auth, g, db
from api.models.media_contents_model import TypeMediaModel, MediaContentModel
from api.sсhemas.media_contents_schema import MediaContentsSchema, MediaContentsRequestSchema
from flask_apispec import marshal_with, use_kwargs, doc


@doc(description='Api for media', tags=['Media'])
class MediaListResource(MethodResource):
    @auth.login_required
    @doc(security=[{"basicAuth": []}])
    @marshal_with(MediaContentsSchema(many=True), code=200)
    @doc(summary='Get all media')
    @doc(description='Full: Get all media')
    def get(self):
        media = MediaContentModel.query.filter(MediaContentModel.id_user == g.user.id_user).all()
        return media, 200

    @auth.login_required
    @doc(description='create new media')
    @marshal_with(MediaContentsSchema, code=201)
    @use_kwargs(MediaContentsRequestSchema, location='json')
    @doc(security=[{"basicAuth": []}])
    def post(self, **kwargs):
        root, ext = os.path.splitext(kwargs["name_file"][-6:])
        ext = ext.lower()
        type_media = TypeMediaModel.query.filter(TypeMediaModel.extension == ext.strip('.')).first()
        if not type_media:
            return f"error extension file: {kwargs['file_name']}", 400
        media = MediaContentModel(id_user=g.user.id_user, id_type_media=type_media.id_type_media, **kwargs)
        media.save()
        return media, 201
