from api import ma
from api.models.posts_model import PostsModel

#       schema        flask-restful
# object ------>  dict ----------> json

# Сериализация ответа(response)
from api.sсhemas.media_contents_schema import MediaContentsSchema


class PostSchema(ma.SQLAlchemySchema):
    class Meta:
        model = PostsModel

    id_post = ma.auto_field(required=True)
    text = ma.auto_field(required=True)
    media = ma.Nested(MediaContentsSchema, many=True)


# Десериализация запроса(request)
class PostRequestSchema(ma.SQLAlchemySchema):
    class Meta:
        model = PostsModel

    text = ma.Str()
    id_media = ma.Int()
