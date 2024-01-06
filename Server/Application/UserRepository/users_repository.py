from EasyToCacheLib.easy_to_cache import Cache
from Server.Domain.user import User
import uuid


class UsersRepository:
    __instance = None

    def __init__(self, user_data_path, user_passwords_path):
        if self.__initialized:
            return
        self.__initialized = True

        print("INIT UsersRepository")
        self._data_path = user_data_path
        self._passwords_path = user_passwords_path

        self.passwords = Cache(user_passwords_path + "passwords.json", True, decrypt_user, cache_user)
        self.data = Cache(user_data_path + "users.json", True, decrypt_user, cache_user)

    def get_user_by_login_and_password(self, login: str, password: str):
        user_password = self.passwords.try_get(login)
        if not user_password:
            return None
        if password in user_password.keys():
            return user_password[password]
        return None

    def register_user(self, login: str, password: str):
        new_user = self.passwords.try_get(login)
        if new_user:
            return None
        new_user = User(str(uuid.uuid4()))
        self.passwords.add(login, {password: new_user}).write_to_json()
        self.data.add(new_user.user_id, new_user).write_to_json()
        return new_user

    def get_user_by_id(self, user_id) -> User:
        return self.data.try_get(user_id)

    def delete_user_by_id(self, user_id):
        if self.data.try_get(user_id):
            self.data.remove(user_id).write_to_json()

    def clear(self):
        self.data.clear().write_to_json()
        self.passwords.clear().write_to_json()

    def update_json(self):
        self.passwords.write_to_json()
        self.data.write_to_json()

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__initialized = False
        return cls.__instance


def cache_user(obj):
    if isinstance(obj, User):
        return {
            "__type__": "user",
            "isoformat": [obj.user_id, obj.liked, obj.playlists]
        }
    return None


def decrypt_user(obj):
    if "__type__" in obj and obj["__type__"] == "user":
        return User(*obj["isoformat"])
    return None
