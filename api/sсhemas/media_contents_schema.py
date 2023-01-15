from api import ma
from api.models.media_contents_model import MediaContentModel, TypeMediaModel


#       schema        flask-restful
# object ------>  dict ----------> json

# Сериализация ответа(response)
class MediaContentsSchema(ma.SQLAlchemySchema):
    class Meta:
        model = MediaContentModel

    id_media = ma.auto_field(required=True)
    id_type_media = ma.auto_field(required=True)
    date_download = ma.auto_field(required=True)


# Десериализация запроса(request)
class MediaContentsRequestSchema(ma.SQLAlchemySchema):
    class Meta:
        model = TypeMediaModel

    description = ma.Str()
    name_file = ma.Str(required=True)



