from EasyToCacheLib.easy_to_cache import Cache
from Server.Domain.user import User
import uuid


class UsersRepository:
    def __init__(self, cache_path, passwords_path):
        self._cache_path = cache_path
        self._passwords_path = passwords_path

        self.passwords = Cache(passwords_path + "passwords.json", True)
        self.cache = Cache(cache_path + "users.json", True)

    def get_user_by_login_and_password(self, login: str, password: str):
        return self.passwords.try_get((login, password))

    def register_user(self, login: str, password: str):
        new_user = self.passwords.try_get((login, password))
        if not new_user:
            new_user = User(str(uuid.uuid4()))
            self.passwords.add((login, password), new_user)
            self.cache.add(new_user.user_id, new_user)
        return new_user

    def get_user_by_id(self, user_id):
        return self.cache.try_get(user_id)

    def delete_user_by_id(self, user_id):
        self.cache.remove(user_id).write_to_json()

    def clear(self):
        self.cache.clear().write_to_json()
