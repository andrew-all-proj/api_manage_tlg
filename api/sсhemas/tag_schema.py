from api import ma
from api.models.media_tags_model import TagModel



#       schema        flask-restful
# object ------>  dict ----------> json

# Сериализация ответа(response)


class TagSchema(ma.SQLAlchemySchema):
    class Meta:
        model = TagModel

    id_tag = ma.auto_field(required=True)
    tag_name = ma.auto_field(required=True)


class TagListSchema(ma.SQLAlchemySchema):
    class Meta:
        model = TagModel

    id_channel = ma.auto_field(required=True)
    tag_name = ma.auto_field(required=True)
    id_tag = ma.auto_field(required=True)


class TagCreateSchema(ma.SQLAlchemySchema):
    class Meta:
        model = TagModel

    tag_name = ma.auto_field(required=True)
    id_channel = ma.auto_field(required=True)

class TagChangeSchema(ma.SQLAlchemySchema):
    class Meta:
        model = TagModel

    tag_name = ma.auto_field(required=True)
