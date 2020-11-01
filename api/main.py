import logging

from aiohttp import web

from src import settings
from src.server import make_server


def main():
    app = make_server()

    logger = logging.getLogger(__name__)
    logger.info(
        'Server is starting on %s : %s',
        settings.SERVER_HOST,
        settings.SERVER_PORT,
    )

    web.run_app(
        app,
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        access_log_format=settings.AIOHTTP_ACCESS_LOG_FORMAT,
    )


if __name__ == '__main__':
    main()
