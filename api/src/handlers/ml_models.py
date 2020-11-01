from enum import Enum

from aiohttp import web
from aiohttp.web_request import Request
from aiohttp.web_response import Response
from aiohttp_apispec import docs, request_schema
from marshmallow import Schema, fields
from marshmallow_enum import EnumField

from src import settings
from src.ml_models.download import download_model


class ModelType(Enum):
    book = 'book'
    club = 'club'
    event = 'event'


class MlModelSchema(Schema):
    model_key = fields.String(description='Model key in bucket', required=True)
    model_kind = EnumField(ModelType, required=True)


@docs(
    tags=['tools'],
    summary='Set new model',
    description='Pass new model key and server will use it',
    produces='application/json',
    responses={
        200: {
            'description': 'Successful operation',
        },
        404: {
            'description': 'Model not found',
        },
        422: {
            'description': 'Validation error',
        },
    },
)
@request_schema(MlModelSchema())
async def set_model(request: Request) -> Response:
    model = await request.json()
    model_key = model['model_key']
    model_kind = model['model_kind']

    await download_model(model_key)
    if model_kind == ModelType.book.value:
        settings.MODEL_BOOK_KEY = model_key
    elif model_kind == ModelType.club.value:
        settings.MODEL_CLUB_KEY = model_key
    elif model_kind == ModelType.event.value:
        settings.MODEL_EVENT_KEY = model_key

    return web.json_response({
        'status': 'ok'
    })
