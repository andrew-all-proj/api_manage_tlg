from api import ma
from api.models.feedback_bots.feedback_bots_model import FeedbackBotsModel
from api.sсhemas.users_to_feedback_schema import UsersToFeedbackBotSchema


class FeedbackBotsSchema(ma.SQLAlchemySchema):
    class Meta:
        model = FeedbackBotsModel

    id_feedback_bot = ma.Int(required=True)
    token_bot = ma.Str(required=True)
    name_bot = ma.Str(required=True)
    users_feedback = ma.Nested(UsersToFeedbackBotSchema(many=True))


class FeedbackBotsPostSchema(ma.SQLAlchemySchema):
    class Meta:
        model = FeedbackBotsModel

    token_bot = ma.auto_field(required=True)
    name_bot = ma.auto_field(required=True)


