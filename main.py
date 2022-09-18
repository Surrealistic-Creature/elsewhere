# -*- coding: utf-8 -*-
import json
import uvicorn
from starlette.applications import Starlette
from starlette.responses import JSONResponse, RedirectResponse
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
import imghdr
import hashlib

templates = Jinja2Templates(directory='templates')


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
    # response.set_cookie(key='mycookie', value='elsewhere', path="/")
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


async def log_out(request):
    token = request.cookies.get('token')
    logout = request.app.state.logged_users.pop(token, None)
    print(logout)
    return RedirectResponse(url='/', status_code=303)


async def login_route(request):
    login = await request.form()
    try:
        user = database.sign_in(login)
    except database.SignInError as exc:
        return JSONResponse({'message': str(exc)})
    token = str(uuid.uuid4())
    request.app.state.logged_users[token] = user
    print(user, 'here user data')
    print(request.app.state.logged_users)
    response = RedirectResponse(url=f'/users/{user.id}', status_code=303)
    response.set_cookie(key='token', value=token, path="/", max_age=60*60*24)
    return response


async def logged_user(request):
    token = request.cookies.get('token')
    logged_user = None
    if token is not None:
        logged_user = request.app.state.logged_users.get(token)
    user_id = request.path_params['user_id']
    wuser = database.get_user_by_id(user_id)
    response = templates.TemplateResponse('user.html', {
        'request': request,
        'cookie': request.cookies.get('mycookie'),
        'user': logged_user,
        'wuser': wuser,
        'self_viewing': False if logged_user is None
        else logged_user.id == user_id
    })
    # response.set_cookie(key='mycookie', value='elsewhere', path="/")
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


async def upload_file(request):
    token = request.cookies.get('token')
    logged_user = None
    if token is not None:
        logged_user = request.app.state.logged_users.get(token)
    if logged_user is None:
        return JSONResponse(
            {'message': 'GO AWAY'}, status_code=403)
    upload = await request.form()
    contents = await upload["avatar"].read()
    detected_filetype = imghdr.what(None, h=contents)
    allowed_types = ['jpeg', 'png']
    if detected_filetype not in allowed_types:
        return JSONResponse({'message': 'bad filetype'})
    hash_object = hashlib.sha1(contents)
    hash_str = hash_object.hexdigest()
    imgdir = "uploads/avatars"
    filename = f"{hash_str}.{detected_filetype}"
    with open(f"{imgdir}/{filename}", "wb") as binary_file:
        binary_file.write(contents)
    database.add_avatar(logged_user.id, filename)
    return JSONResponse({'message': detected_filetype})


routes = [
    Route('/', endpoint=homepage),
    Route('/users/{user_id:int}', endpoint=logged_user),
    Route('/login_route', endpoint=login_route, methods=['POST']),
    Route('/logout', endpoint=log_out, methods=['POST']),
    Route('/sign_up', endpoint=sign_up, methods=['POST']),
    WebSocketRoute('/ws', websocket_endpoint),
    Route('/vkpstgr', endpoint=vk_pstgre),
    Route('/psqlsh', endpoint=show_db),
    Route('/rmflst', endpoint=remove_flist),
    Route('/filter/{city}', endpoint=find_by_city),
    Route('/upload_file', endpoint=upload_file, methods=['POST']),
    Mount('/static', StaticFiles(directory='static'), name='static'),
    Mount('/uploads', StaticFiles(directory='uploads'), name='uploads')
]

# , on_startup=[init_db]
app = Starlette(debug=True, routes=routes,)
app.state.logged_users = {}

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000, loop='uvloop')
