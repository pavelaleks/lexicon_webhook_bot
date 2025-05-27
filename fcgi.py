# fcgi.py
from webhook import create_app
from aiohttp import web
import asyncio

async def app_handler(environ, start_response):
    app = await create_app()
    return await app._handle(environ, start_response)

def application(environ, start_response):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(app_handler(environ, start_response))
