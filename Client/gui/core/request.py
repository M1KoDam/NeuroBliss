from .data import User, ConnectionType, Singleton
from .event import DATA_MANAGER
import Client.Application.client_api as api
import httpx


class Sender(metaclass=Singleton):
    @staticmethod
    def try_make_registration_request(login: str, password: str) -> tuple[bool, str]:
        register_item = api.register_user(login=login, password=password)
        if register_item is httpx.ConnectError:
            print('Servers is unreachable')
            DATA_MANAGER.connection = ConnectionType.Offline
            return False, None

        is_success = register_item["message"]

        user_id = None
        if is_success:
            DATA_MANAGER.connection = ConnectionType.Online
            user_id = register_item["id"]

        return is_success, user_id

    @staticmethod
    def try_make_sing_in_request(login: str, password: str) -> tuple[bool, str]:
        register_item = api.login_user(login=login, password=password)
        if register_item is httpx.ConnectError:
            print('Servers is unreachable')
            DATA_MANAGER.connection = ConnectionType.Offline
            return False, None

        is_success = register_item["message"]

        user_id = None
        if is_success:
            DATA_MANAGER.connection = ConnectionType.Online
            user_id = register_item["id"]

        return is_success, user_id

    @staticmethod
    def send_get_music_generation_request(user_id: str, genres: list[str]) -> tuple[bool, str]:
        register_item = api.get_music_generation(user_id, genres)
        if register_item is httpx.ConnectError:
            print('Servers is unreachable')
            DATA_MANAGER.connection = ConnectionType.Offline
            return False, None

        is_success = register_item["message"]

        user_id = None
        if is_success:
            DATA_MANAGER.connection = ConnectionType.Online
            user_id = register_item["id"]

        return is_success, user_id

