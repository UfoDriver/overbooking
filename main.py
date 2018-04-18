import asyncio
from aiohttp import web

from app import create_app


app = create_app(asyncio.get_event_loop())
web.run_app(app, port=8000)
