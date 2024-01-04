from EasyToCacheLib.easy_to_cache import Cache
from Server.Domain.user import User
import uuid


class UsersRepository:
    def __init__(self, cache_path, passwords_path):
        self._cache_path = cache_path
        self._passwords_path = passwords_path

        self.passwords = Cache(passwords_path + "passwords.json", True).set_json_handlers(decrypt_user, cache_user)
        self.cache = Cache(cache_path + "users.json", True).set_json_handlers(decrypt_user, cache_user)

    def get_user_by_login_and_password(self, login: str, password: str):
        return self.passwords.try_get(f"{login} {password}")

    def register_user(self, login: str, password: str):
        new_user = self.passwords.try_get(f"{login} {password}")
        if new_user:
            return None
        new_user = User(str(uuid.uuid4()))
        self.passwords.add(f"{login} {password}", new_user).write_to_json()
        self.cache.add(new_user.user_id, new_user).write_to_json()
        return new_user

    def get_user_by_id(self, user_id):
        return self.cache.try_get(user_id)

    def delete_user_by_id(self, user_id):
        if self.cache.try_get(user_id):
            self.cache.remove(user_id).write_to_json()

    def clear(self):
        self.cache.clear().write_to_json()


def cache_user(obj):
    if isinstance(obj, User):
        return {
            "__type__": "musicitem",
            "isoformat": [obj.user_id]
        }
    return None


def decrypt_user(obj):
    if "__type__" in obj and obj["__type__"] == "musicitem":
        return User(*obj["isoformat"])
    return None
