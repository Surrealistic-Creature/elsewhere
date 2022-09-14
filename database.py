import pprint
import outsource
from postgredb import VKFriend, Session, City, UserEntity
from starlette.datastructures import FormData
from typing import Optional


def take_to_pstgr():

    session = Session()

    vkapi = outsource
    some_info = vkapi.main_auth()
    flist = some_info.get('items')
    for smprsn in flist:
        pprint.pprint(smprsn)
        existed_person = session.query(VKFriend).filter(
            VKFriend.vk_id == smprsn['id']).first()
        if existed_person:
            continue
        city_id = smprsn['city']['id'] if smprsn.get('city') else None
        if city_id is None:
            city = None
        else:
            city = session.query(City).get(city_id)
            if city is None:
                new_city = City(
                    id=smprsn['city']['id'],
                    title=smprsn['city']['title']
                    )
                session.add(new_city)
                session.commit()
                city = new_city
        pfriend = VKFriend(
            first_name=smprsn['first_name'],
            vk_id=smprsn['id'],
            last_name=smprsn['last_name'],
            sex=smprsn['sex'],
            nickname=smprsn['nickname'],
            domain=smprsn['domain'],
            bdate=smprsn.get('bdate'),
            city=city
        )
        session.add(pfriend)
    session.commit()
    session.close()


def remove_score():
    session = Session()
    session.query(VKFriend).delete()
    session.commit()


def show_postgre():
    session = Session()
    users = session.query(VKFriend).all()
    vkfriends_list = []
    for user in users:
        user_dict = {
            "first_name": user.first_name,
            "domain": user.domain,
            "last_name": user.last_name,
            "sex": user.sex,
            "vk_id": user.vk_id,
            "bdate": user.bdate}
        vkfriends_list.append(user_dict)
    session.close()

    return vkfriends_list


def show_partialy():
    session = Session()
    show = session.query(VKFriend).filter(
        VKFriend.city.has(title='Москва')).all()
    vkflist = []
    for user in show:
        user_dict = {
            "first_name": user.first_name,
            "domain": user.domain,
            "last_name": user.last_name,
            "sex": user.sex,
            "vk_id": user.vk_id,
            "bdate": user.bdate}
        vkflist.append(user_dict)
    session.close()
    return vkflist


def get_by_city(city_title):
    session = Session()
    users = session.query(VKFriend).filter(
        VKFriend.city.has(title=city_title)).all()
    vkfriends_list = []
    for user in users:
        user_dict = {
            "first_name": user.first_name,
            "domain": user.domain,
            "last_name": user.last_name,
            "sex": user.sex,
            "vk_id": user.vk_id,
            "bdate": user.bdate}
        vkfriends_list.append(user_dict)
    session.close()
    return vkfriends_list


def sign_up(form: FormData):
    session = Session()
    login = form.get('login').strip()
    if len(login) < 6:
        return "strongly required login"
    password = form.get('pass').strip()
    if len(password) < 6:
        return "strongly required password"
    username = form.get('username')
    email = form.get('email')
    existing_user = session.query(UserEntity).filter(
        UserEntity.login == login).first()
    if existing_user:
        return "sorry, User with this name already exist"
    else:
        new_user = UserEntity(
            login=login,
            password=password,
            username=username,
            email=email
            )
        session.add(new_user)
    session.commit()
    session.close()
    return "User Created"


class SignInError(Exception):
    pass


def sign_in(form: FormData) -> Optional[UserEntity]:
    session = Session()
    login = form.get('login').strip()
    if len(login) < 5:
        raise SignInError('strongly required login')
    password = form.get('pass').strip()
    if len(password) < 5:
        raise SignInError('strongly required password')
    signin = session.query(UserEntity).filter(
        UserEntity.login == login,
        UserEntity.password == password).first()
    if signin is None:
        raise SignInError('user not exist')
    return signin
