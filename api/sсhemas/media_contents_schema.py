from api import ma
from api.models.media_contents_model import MediaContentModel, TypeMediaModel
from api.sсhemas.tag_schema import TagSchema
from api.sсhemas.type_media_schema import TypeMediaSchema


class MediaContentsSchema(ma.SQLAlchemySchema):
    class Meta:
        model = MediaContentModel

    id_media = ma.auto_field(required=True)
    type_media = ma.Nested(TypeMediaSchema)
    date_download = ma.auto_field(required=True)
    description = ma.auto_field()
    tags = ma.Nested(TagSchema, many=True)


class MediaContentsRequestSchema(ma.SQLAlchemySchema):
    class Meta:
        model = TypeMediaModel

    description = ma.Str()
    name_file = ma.Str(required=True)


class MediaChangeSchema(ma.SQLAlchemySchema):
    class Meta:
        model = TypeMediaModel

    description = ma.Str(required=True)
