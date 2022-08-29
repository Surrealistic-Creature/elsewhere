# -*- coding: utf-8 -*-
import json
import uvicorn
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route, Mount, WebSocketRoute
# from motor.motor_asyncio import AsyncIOMotorClient
# from starlette.responses import Response
# from jinja2 import Environment, PackageLoader, select_autoescape
# from starlette.websockets import WebSocket
# from starlette.endpoints import HTTPEndpoint, WebSocketEndpoint
from starlette.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
import database
import uuid

templates = Jinja2Templates(directory='templates')

"""
async def init_db():
    client = AsyncIOMotorClient('mongodb://localhost:27017')
    app.state.db = client.others
"""

"""
#   if request.cookies.get('mycookie'):
#   login = request.query_params.get('login')
#   password = request.query_params.get('pass')
#   print(login)
"""


async def init_db():
    database.show_postgre()
    return JSONResponse({'message': 'ok'})


async def homepage(request):
    token = request.cookies.get('token')
    user = None
    if token is not None:
        user = request.app.state.logged_users.get(token)
    response = templates.TemplateResponse('index.html', {
        'request': request,
        'cookie': request.cookies.get('mycookie'),
        'user': user
    })
    response.set_cookie(key='mycookie', value='elsewhere', path="/")
    return response


# переписать на postgresql
async def websocket_endpoint(websocket):
    await websocket.accept()
    hello = database.show_partialy()
    send_to = json.dumps(hello, ensure_ascii=False)
    # count = await database.do_count_docs(websocket.app.state.db)
    await websocket.send_text(send_to)
    while True:
        try:
            hell = await websocket.receive_text()
            print('hello there', hell)
        except Exception:
            print('here')
            break


async def sign_up(request):
    login = await request.form()
    new_user = database.sign_up(login)
    return JSONResponse({'message': new_user})


async def login_route(request):
    login = await request.form()
    user = database.sign_in(login)
    if user is None:
        return JSONResponse({'message': 'sorry for what'})
    token = str(uuid.uuid4())
    request.app.state.logged_users[token] = user
    print(request.app.state.logged_users)
    response = JSONResponse({'message': token})
    response.set_cookie(key='token', value=token, path="/")
    return response


async def vk_pstgre(_request):
    database.take_to_pstgr()
    return JSONResponse({'message': 'ok'})


async def show_db(_request):
    flist = database.show_postgre()
    return JSONResponse({'friends': flist})


async def remove_flist(_request):
    database.remove_score()
    flist = database.show_postgre()
    return JSONResponse({'friends': flist})


async def find_by_city(request):
    city_title = request.path_params['city']
    flist = database.get_by_city(city_title)
    return JSONResponse({'friends': flist})


routes = [
    Route('/', endpoint=homepage),
    Route('/login_route', endpoint=login_route, methods=['POST']),
    Route('/sign_up', endpoint=sign_up, methods=['POST']),
    # Route('/vk_connect', endpoint=vk_connect),
    # Route('/psh', endpoint=pushing_people),
    # Route('/rm_docs', endpoint=remove_docs),
    # Route('/show', endpoint=show_people),
    # Route('/import', endpoint=importing),
    WebSocketRoute('/ws', websocket_endpoint),
    Route('/vkpstgr', endpoint=vk_pstgre),
    Route('/psqlsh', endpoint=show_db),
    Route('/rmflst', endpoint=remove_flist),
    Route('/filter/{city}', endpoint=find_by_city),
    Mount('/static', StaticFiles(directory='static'), name='static')]

# , on_startup=[init_db]
app = Starlette(debug=True, routes=routes,)
app.state.logged_users = {}

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000, loop='uvloop')
