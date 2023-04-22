from flask_apispec import marshal_with, use_kwargs, doc
from flask_apispec.views import MethodResource
from flask_pyjwt import require_token, current_token
from sqlalchemy import and_

from api.models.feedback_bots.feedback_bots_model import FeedbackBotsModel
from api.sсhemas.feedback_bots_schema import FeedbackBotsSchema, FeedbackBotsPostSchema


def query_feedback_bot(id_user):
    return FeedbackBotsModel.query.filter(and_(FeedbackBotsModel.id_admin_user == id_user,
                                               FeedbackBotsModel.is_archive == False))


@doc(description='Api for feedback bots', tags=['Feedback Bots'])
class FeedBackBotsListResource(MethodResource):
    @require_token()
    @doc(security=[{"bearerAuth": []}])
    @marshal_with(FeedbackBotsSchema)
    @use_kwargs(FeedbackBotsPostSchema, location='json')
    @doc(summary='Create new feedback bot')
    @doc(description='Full: Create new feedback bot')
    def post(self, **kwargs):
        feedback_bot = FeedbackBotsModel(id_admin_user=current_token.scope, **kwargs)
        if not feedback_bot.save():
            return {"error": "save in bd"}, 400
        return feedback_bot, 201

    @require_token()
    @doc(security=[{"bearerAuth": []}])
    @marshal_with(FeedbackBotsSchema(many=True))
    @doc(summary='Get all feedback bots')
    @doc(description='Full: Get all feedback bots')
    def get(self):
        feedback_bot = query_feedback_bot(current_token.scope).all()
        if not feedback_bot:
            return {"error": "not found"}, 404
        return feedback_bot, 200


@doc(description='Api for feedback bots', tags=['Feedback Bots'])
class FeedBackBotResource(MethodResource):
    @require_token()
    @doc(security=[{"bearerAuth": []}])
    @marshal_with(FeedbackBotsSchema)
    @doc(summary='Get feedback bot by id')
    @doc(description='Full: Get feedback bot by id')
    def get(self, id_feedback_bot):
        feedback_bot = query_feedback_bot(current_token.scope).filter(
            FeedbackBotsModel.id_feedback_bot == id_feedback_bot).first()
        if not feedback_bot:
            return {"error": "not found"}, 404
        return feedback_bot, 201

    @require_token()
    @doc(security=[{"bearerAuth": []}])
    @marshal_with(FeedbackBotsPostSchema)
    @use_kwargs(FeedbackBotsPostSchema, location='json')
    @doc(summary='Change data feedback bots by id')
    @doc(description='Full: Change data feedback bots by id')
    def put(self, id_feedback_bot, **kwargs):
        feedback_bot = query_feedback_bot(current_token.scope).filter \
            (FeedbackBotsModel.id_feedback_bot == id_feedback_bot).first()
        if not feedback_bot:
            return {"error": "not found"}, 404
        feedback_bot.token_bot = kwargs.get('token_bot') or feedback_bot.token_bot
        feedback_bot.name_bot = kwargs.get('name_bot') or feedback_bot.name_bot
        if not feedback_bot.save():
            return {"error": "update data base"}, 400
        return feedback_bot, 200

    @require_token()
    @doc(security=[{"bearerAuth": []}])
    @doc(summary='Delete feedback bots by id')
    @doc(description='Full: Delete feedback bots by id')
    def delete(self, id_feedback_bot):
        feedback_bot = query_feedback_bot(current_token.scope).filter \
            (FeedbackBotsModel.id_feedback_bot == id_feedback_bot).first()
        if not feedback_bot:
            return {"error": "not found"}, 404
        feedback_bot.to_archive()
        if not feedback_bot.save():
            return {"error": "update data base"}, 400
        return {}, 200
