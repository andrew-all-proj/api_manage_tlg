from api import ma

from api.models.media_contents_model import TypeMediaModel


class TypeMediaSchema(ma.SQLAlchemySchema):
    class Meta:
        model = TypeMediaModel

    type_media = ma.auto_field()