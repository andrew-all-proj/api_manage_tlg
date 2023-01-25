from api import ma
from api.models.media_contents_model import MediaContentModel, TypeMediaModel
from api.sсhemas.tag_schema import TagSchema
from api.sсhemas.type_media_schema import TypeMediaSchema
from marshmallow import fields
#       schema        flask-restful
# object ------>  dict ----------> json

# Сериализация ответа(response)
from config import Config


class MediaContentsSchema(ma.SQLAlchemySchema):
    class Meta:
        model = MediaContentModel

    id_media = ma.auto_field(required=True)
    type_media = ma.Nested(TypeMediaSchema)
    date_download = ma.auto_field(required=True)
    description = ma.auto_field()
    tags = ma.Nested(TagSchema, many=True)


# Десериализация запроса(request)
class MediaContentsRequestSchema(ma.SQLAlchemySchema):
    class Meta:
        model = TypeMediaModel

    description = ma.Str()
    name_file = ma.Str(required=True)


class MediaContentsPostSchema(ma.SQLAlchemySchema):


    image = ma.Str(required=True)