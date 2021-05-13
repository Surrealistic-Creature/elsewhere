# -*- coding: utf-8 -*-


import uvicorn
from motor.motor_asyncio import AsyncIOMotorClient
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route, Mount
from starlette.templating import Jinja2Templates
from jinja2 import Environment, PackageLoader, select_autoescape
from starlette.staticfiles import StaticFiles
from starlette.websockets import WebSocket

import database

templates = Jinja2Templates(directory='templates')

async def init_db():
    client = AsyncIOMotorClient('mongodb://localhost:27017')
    app.state.db = client.others


async def homepage(request):
    await database.insertion(request.app.state.db)
    return templates.TemplateResponse('index.html', {'request' : request})


routes = [
        Route('/', endpoint=homepage),
        Mount('/static', StaticFiles(directory='static'), name='static')]

app = Starlette(debug=True, routes=routes, on_startup=[init_db])

async def ws_test(scope, receive, send):
    websocket = WebSocket(scope=scope, receive=receive, send=send)
    await websocket.accept()
    await websocket.send_text('Hello, world!')
    await websocket.close()

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000, loop='uvloop')
