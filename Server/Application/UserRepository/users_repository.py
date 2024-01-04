from EasyToCacheLib.easy_to_cache import Cache


class UsersRepository:
    def __init__(self, cache_path):
        self._cache_path = cache_path
        self.data = Cache(cache_path+"users.json", True)

    def get_user_by_id(self, user_id):
        return self.data.try_get(user_id)

    def delete_user_by_id(self, user_id):
        self.data.remove(user_id).write_to_json()

    def clear(self):
        self.data.clear().write_to_json()
