from EasyToCacheLib.easy_to_cache import Cache


class Repository:
    def __init__(self, data_path, cache_path):
        self._data_path = data_path
        self._cache_path = cache_path
        self.data = Cache(cache_path+"data.json", True)

