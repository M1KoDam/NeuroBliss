from .data import ConnectionType, Singleton
from .event import DATA_MANAGER
import Client.Application.client_api as api
import httpx


class Sender(metaclass=Singleton):
    @staticmethod
    def try_make_registration_request(login: str, password: str) -> tuple[bool | None, str | None]:
        register_item = api.register_user(login=login, password=password)
        if register_item is httpx.ConnectError:
            print('Servers is unreachable')
            DATA_MANAGER.connection = ConnectionType.Offline
            return None, None

        is_success = register_item["message"]

        user_id = None
        if is_success:
            DATA_MANAGER.connection = ConnectionType.Online
            user_id = register_item["id"]

        return is_success, user_id

    @staticmethod
    def try_make_sing_in_request(login: str, password: str) -> tuple[bool | None, str | None]:
        register_item = api.login_user(login=login, password=password)
        if register_item is httpx.ConnectError:
            print('Servers is unreachable')
            DATA_MANAGER.connection = ConnectionType.Offline
            return None, None

        is_success = register_item["message"]

        user_id = None
        if is_success:
            DATA_MANAGER.connection = ConnectionType.Online
            user_id = register_item["id"]

        return is_success, user_id

    @staticmethod
    def try_send_get_music_generation_request(user_id: str, genre: str) -> tuple[bool | None, str | None, str | None]:
        # register_item = api.get_music_generation(user_id, genres)
        register_item = api.get_music_by_id(music_id='cd91fbd3-e155-471a-a3c2-fa29b5cdb227', user_id=user_id)
        if register_item is httpx.ConnectError:
            print('Servers is unreachable')
            DATA_MANAGER.connection = ConnectionType.Offline
            return None, None, None

        is_success = register_item["status"]
        path = register_item["path"] if is_success else None
        music_id = register_item['music_id'] if is_success else None

        return is_success, path, music_id

