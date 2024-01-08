from .data import User, AppData, Singleton
from .event import ConnectionType, EventSolver, EVENT_HANDLER, DataManager, EventType
from os import getcwd
from pathlib import Path


class CacheHandler(EventSolver, metaclass=Singleton):
    def __init__(self):
        EVENT_HANDLER.subscribe(self, EventType.OnUserChanged)

    def notify(self, event: EventType, data_manager: DataManager):
        if data_manager.connection is ConnectionType.Online:
            self.write_to_cache(data_manager.app_data)

    @staticmethod
    def write_to_cache(app_data: AppData) -> None:
        print('caching....')
        path = CacheHandler.get_path_to_user_info()
        with open(path, 'w') as file:
            parts = app_data.get_user_info()
            for part in parts:
                file.write(part + '\n')
                file.flush()

    @staticmethod
    def try_read_from_cache() -> User | None:
        print('reading....')
        path = CacheHandler.get_path_to_user_info()
        try:
            with open(path, 'r') as file:
                login = file.readline().split('Login=')[1].strip()
                password = file.readline().split('Password=')[1].strip()
                avatar_color = file.readline().split('AvatarColor=')[1].strip()
                original_login = file.readline().split('OriginalLogin=')[1].strip()
                original_password = file.readline().split('OriginalPassword=')[1].strip()
                user_id = file.readline().split('Id=')[1].strip()

                if original_login == 'None' or original_password == 'None' or user_id == 'None':
                    return None
                return User(
                    Login=login, Password=password, AvatarColor=avatar_color,
                    OriginalLogin=original_login, OriginalPassword=original_password, Id=user_id
                )

        except (FileNotFoundError, IndexError, ValueError):
            return None

    @staticmethod
    def get_path_to_user_info() -> Path:
        path = str(
            Path(str(getcwd())) / 'core' / 'cache' / 'user-info.txt'
        )
        if 'gui' not in path:
            path = str(
                Path(str(getcwd())) / 'gui' / 'core' / 'cache' / 'user-info.txt'
            )

        return Path(path)
