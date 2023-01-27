from marshmallow import fields

from api import ma
from api.models.posts_model import PostsModel
from api.sсhemas.media_contents_schema import MediaContentsSchema


#       schema        flask-restful
# object ------>  dict ----------> json

# Сериализация ответа(response)


class PostSchema(ma.SQLAlchemySchema):
    class Meta:
        model = PostsModel

    id_post = ma.auto_field(required=True)
    text = ma.auto_field(required=True)
    media = ma.Nested(MediaContentsSchema, many=True)
    date_create = ma.auto_field(required=True)
    data_update = ma.auto_field(required=True)


# Десериализация запроса(request)
class PostCreatetSchema(ma.SQLAlchemySchema):
    class Meta:
        model = PostsModel

    text = ma.Str(required=False)
