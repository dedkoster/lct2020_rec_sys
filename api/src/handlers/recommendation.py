from aiohttp import web
from aiohttp.web_request import Request
from aiohttp.web_response import Response
from aiohttp_apispec import docs, querystring_schema
from marshmallow import fields, Schema

from src.ml_models.run import run_on_last_book_model, \
    run_on_last_club_model, run_on_last_event_model


class UserRecommendationSchema(Schema):
    id = fields.String(description='User unique ID', required=True)
    top_n = fields.Integer(description='Top N features will be predicted',
                           required=False, default=20)


class BookRecommendationSchema(Schema):
    # TODO: add strict schema of response
    pass


class ClubRecommendationSchema(Schema):
    # TODO: add strict schema of response
    pass


class EventRecommendationSchema(Schema):
    # TODO: add strict schema of response
    pass


@docs(
    tags=['recommendation'],
    summary='Get book recommendation for user',
    description='Returns content recommendation for user',
    produces='application/json',
    responses={
        200: {
            'description': 'Successful recommendation',
            'schema': BookRecommendationSchema,
        },
        404: {
            'description': 'User not found',
        },
        422: {
            'description': 'Validation error',
        },
    },
)
@querystring_schema(UserRecommendationSchema())
async def get_book_recommendation(request: Request) -> Response:
    user_id = request.rel_url.query.get('id')

    result = await run_on_last_book_model(user_id)

    return web.json_response({
        'result': result
    })


@docs(
    tags=['recommendation'],
    summary='Get club recommendation for user',
    description='Returns content recommendation for user',
    produces='application/json',
    responses={
        200: {
            'description': 'Successful recommendation',
            'schema': ClubRecommendationSchema,
        },
        404: {
            'description': 'User not found',
        },
        422: {
            'description': 'Validation error',
        },
    },
)
@querystring_schema(UserRecommendationSchema())
async def get_club_recommendation(request: Request) -> Response:
    user_id = request.rel_url.query.get('id')

    result = await run_on_last_club_model(user_id)

    return web.json_response({
        'result': result
    })


@docs(
    tags=['recommendation'],
    summary='Get event recommendation for user',
    description='Returns content recommendation for user',
    produces='application/json',
    responses={
        200: {
            'description': 'Successful recommendation',
            'schema': EventRecommendationSchema,
        },
        404: {
            'description': 'User not found',
        },
        422: {
            'description': 'Validation error',
        },
    },
)
@querystring_schema(UserRecommendationSchema())
async def get_event_recommendation(request: Request) -> Response:
    user_id = request.rel_url.query.get('id')

    result = await run_on_last_event_model(user_id)

    return web.json_response({
        'result': result
    })
