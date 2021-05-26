# -*- coding: utf-8 -*-

import uvicorn
from motor.motor_asyncio import AsyncIOMotorClient
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route, Mount, WebSocketRoute
from starlette.templating import Jinja2Templates
from jinja2 import Environment, PackageLoader, select_autoescape
from starlette.staticfiles import StaticFiles
from starlette.websockets import WebSocket
from starlette.endpoints import HTTPEndpoint, WebSocketEndpoint
import database


templates = Jinja2Templates(directory='templates')

async def init_db():
    client = AsyncIOMotorClient('mongodb://localhost:27017')
    app.state.db = client.others

async def homepage(request):
    return templates.TemplateResponse('index.html', {'request' : request})

async def websocket_endpoint(websocket):
    await websocket.accept()
    hello = await database.outload(websocket.app.state.db)
    count = await database.do_count(websocket.app.state.db)
    await websocket.send_json(hello)
    while True:
        try:
            hello = await websocket.receive_text()
            print(hello)
        except Exception:
            print('here')
            break


routes = [
        Route('/', endpoint=homepage),
        WebSocketRoute('/ws', websocket_endpoint),
        Mount('/static', StaticFiles(directory='static'), name='static')]

app = Starlette(debug=True, routes=routes, on_startup=[init_db])

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000, loop='uvloop')
