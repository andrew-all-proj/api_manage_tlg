from api import ma
from api.models.media_tags_model import TagModel



#       schema        flask-restful
# object ------>  dict ----------> json

# Сериализация ответа(response)


class TagSchema(ma.SQLAlchemySchema):
    class Meta:
        model = TagModel

    id_tag = ma.auto_field(required=True)
    name = ma.auto_field(required=True)
