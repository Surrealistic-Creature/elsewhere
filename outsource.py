import vk_api
from config import settings


def auth_handler():
    key = input("Enter authentification code: ")
    remember_device = True
    return key, remember_device


def main_auth():
    vk_session = vk_api.VkApi(
            login=settings['login'],
            password=settings['password'],
            auth_handler=auth_handler,
            app_id=settings['app_id'],
            scope=settings['scope']
            )
    try:
        vk_session.auth()
        vk = vk_session.get_api()
        frendlist = vk.friends.get(
                fields='domain, nickname, sex, bdate, city, country, timezone, education, relation, last_seen')
        return frendlist
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return


if __name__ == '__main__':
    main_auth()
