from api import ma
from api.models.feedback_bots.feedback_bots_model import UsersToFeedbackBot


class UsersToFeedbackBotSchema(ma.SQLAlchemySchema):
    class Meta:
        model = UsersToFeedbackBot

    id_users_to_feedback_bot = ma.auto_field(required=True)
    id_feedback_bot = ma.auto_field(required=True)
    id_user_telegram = ma.auto_field(required=True)
    name_user = ma.auto_field(required=True)


class UsersToFeedbackBotPostSchema(ma.SQLAlchemySchema):
    class Meta:
        model = UsersToFeedbackBot

    id_feedback_bot = ma.auto_field(required=True)
    id_user_telegram = ma.auto_field(required=True)
    name_user = ma.auto_field(required=True)

