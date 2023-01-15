from api import ma


#       schema        flask-restful
# object ------>  dict ----------> json

# Сериализация ответа(response)
from api.models.media_contents_model import TypeMediaModel


class TypeMediaSchema(ma.SQLAlchemySchema):
    class Meta:
        model = TypeMediaModel

    type_media = ma.auto_field()