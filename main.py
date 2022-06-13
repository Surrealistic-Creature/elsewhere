# -*- coding: utf-8 -*-

import uvicorn
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route, Mount
# from motor.motor_asyncio import AsyncIOMotorClient
# from starlette.responses import Response, JSONResponse
# from starlette.routing import Route, Mount, WebSocketRoute
# from jinja2 import Environment, PackageLoader, select_autoescape
# from starlette.websockets import WebSocket
# from starlette.endpoints import HTTPEndpoint, WebSocketEndpoint
from starlette.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
import database


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
    response = templates.TemplateResponse('index.html', {
        'request': request,
        'cookie': request.cookies.get('mycookie')
    })
    response.set_cookie(key='mycookie', value='elsewhere', path="/")
    return response

# переписать на postgresql
"""async def websocket_endpoint(websocket):
    await websocket.accept()
    hello = await database.outload(websocket.app.state.db)
    count = await database.do_count_docs(websocket.app.state.db)
    await websocket.send_json(hello)
    while True:
        try:
            hell = await websocket.receive_text()
            print('hello there', hell)
        except Exception:
            print('here')
            break
"""


async def login_route(request):
    login = await request.form()
    print(login)
    return JSONResponse({'message': 'ok'})


async def show_people(request):
    show = await database.print_people(request.app.state.db)
    print(show)
    return JSONResponse({'message': 'ok'})


async def remove_docs(request):
    await database.del_many(request.app.state.db)
    return JSONResponse({'message': 'ok'})


async def vk_connect(request):
    await database.add_document(request.app.state.db)
    return JSONResponse({'message': 'ok'})


async def pushing_people(request):
    await database.split_doc(request.app.state.db)
    return JSONResponse({'message': 'ok'})


async def importing(request):
    await database.import_friend(request.app.state.db)
    return JSONResponse({'message': 'ok'})


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


# WebSocketRoute('/ws', websocket_endpoint),
routes = [
    Route('/', endpoint=homepage),
    Route('/login_route', endpoint=login_route, methods=['POST']),
    Route('/vk_connect', endpoint=vk_connect),
    Route('/psh', endpoint=pushing_people),
    Route('/rm_docs', endpoint=remove_docs),
    Route('/show', endpoint=show_people),
    Route('/import', endpoint=importing),
    Route('/vkpstgr', endpoint=vk_pstgre),
    Route('/psqlsh', endpoint=show_db),
    Route('/rmflst', endpoint=remove_flist),
    Route('/filter/{city}', endpoint=find_by_city),
    Mount('/static', StaticFiles(directory='static'), name='static')]

# , on_startup=[init_db]
app = Starlette(debug=True, routes=routes,)

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000, loop='uvloop')
