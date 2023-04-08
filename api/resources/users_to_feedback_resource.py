from flask_apispec.views import MethodResource
from flask_pyjwt import require_token, current_token
from api.models.feedback_bots.feedback_bots_model import UsersToFeedbackBot, FeedbackBotsModel
from flask_apispec import marshal_with, use_kwargs, doc
from sqlalchemy import and_

from api.sсhemas.users_to_feedback_schema import UsersToFeedbackBotPostSchema, UsersToFeedbackBotSchema


def user_feedback_bot(id_user):
    return UsersToFeedbackBot.query.filter(and_(FeedbackBotsModel.admin_user_id == id_user))

def query_feedback_bot(id_user):
    return FeedbackBotsModel.query.filter(and_(FeedbackBotsModel.admin_user_id == id_user,
                                               FeedbackBotsModel.is_archive == False))

@doc(description='Api for create users for feedback bot', tags=['Feedback list users'])
class FeedBackBotsUsersListResource(MethodResource):
    @require_token()
    @doc(security=[{"bearerAuth": []}])
    @marshal_with(UsersToFeedbackBotSchema)
    @use_kwargs(UsersToFeedbackBotPostSchema, location='json')
    @doc(summary='Create new user for feedback bot')
    @doc(description='Full: Create new user for feedback bot')
    def post(self, **kwargs):
        user_feedback_bot = UsersToFeedbackBot(**kwargs)
        if not user_feedback_bot.save():
            return {"error": "save in bd"}, 400
        return user_feedback_bot, 201

    @require_token()
    @doc(security=[{"bearerAuth": []}])
    @marshal_with(UsersToFeedbackBotSchema(many=True))
    @doc(summary='Get all list users for feedback bots')
    @doc(description='Full: Get all list users for feedback bots')
    def get(self):
        user_feedback_bot = UsersToFeedbackBot.query \
            .join(FeedbackBotsModel) \
            .filter(and_(FeedbackBotsModel.is_archive == False,
                         FeedbackBotsModel.id_admin_user == current_token.scope)) \
            .all()
        if not user_feedback_bot:
            return {"error": "not found"}, 404
        return user_feedback_bot, 200


@doc(description='Api for create users for feedback bot', tags=['Feedback list users'])
class FeedBackBotsUserResource(MethodResource):
    @require_token()
    @doc(security=[{"bearerAuth": []}])
    @marshal_with(UsersToFeedbackBotSchema)
    @doc(summary='Get user feedback bot by id')
    @doc(description='Full: Get user feedback bot by id')
    def get(self, id_users_to_feedback_bot):
        user_feedback_bot = UsersToFeedbackBot.query.filter\
            (UsersToFeedbackBot.id_users_to_feedback_bot == id_users_to_feedback_bot).first()
        if not user_feedback_bot:
            return {"error": "not found"}, 404
        return user_feedback_bot, 200


    @require_token()
    @doc(security=[{"bearerAuth": []}])
    @marshal_with(UsersToFeedbackBotSchema)
    @use_kwargs(UsersToFeedbackBotPostSchema, location='json')
    @doc(summary='Change data user feedback bot by id')
    @doc(description='Full: Change data user feedback bot by id')
    def put(self, id_users_to_feedback_bot, **kwargs):
        user_feedback_bot = UsersToFeedbackBot.query.filter \
            (UsersToFeedbackBot.id_users_to_feedback_bot == id_users_to_feedback_bot).first()
        if not user_feedback_bot:
            return {"error": "not found"}, 404
        user_feedback_bot.id_feedback_bot = kwargs.get('id_feedback_bot ') or user_feedback_bot.id_feedback_bot
        user_feedback_bot.name_bot = kwargs.get('id_user_telegram') or user_feedback_bot.id_user_telegram
        user_feedback_bot.name_user = kwargs.get('name_user') or user_feedback_bot.name_user
        if not user_feedback_bot.save():
            return {"error": "update data base"}, 400
        return user_feedback_bot, 200


    @require_token()
    @doc(security=[{"bearerAuth": []}])
    @doc(summary='Delete feedback bots by id')
    @doc(description='Full: Delete feedback bots by id')
    def delete(self, id_users_to_feedback_bot):
        user_feedback_bot = UsersToFeedbackBot.query.filter \
            (UsersToFeedbackBot.id_users_to_feedback_bot == id_users_to_feedback_bot).first()
        if not user_feedback_bot:
            return {"error": "not found"}, 404
        user_feedback_bot.to_archive()
        if not user_feedback_bot.delete():
            return {"error": "update data base"}, 400
        return {}, 200
