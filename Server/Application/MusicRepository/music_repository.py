import os
from EasyToCacheLib.easy_to_cache import Cache
from Server.Domain.music_item import MusicItem


class MusicRepository:
    def __init__(self, data_path, cache_path):
        self._data_path = data_path
        self._cache_path = cache_path
        self.data = Cache(cache_path+"music.json", True).set_json_handlers(decrypt_music_item, cache_music_item)

    def add_music(self, music_item: MusicItem):
        self.data.add(music_item.id, music_item).write_to_json()

    def get_music_by_id(self, music_id) -> MusicItem:
        return self.data.try_get(music_id)

    def delete_music_by_id(self, music_id):
        self.data.remove(music_id).write_to_json()

    def clear(self):
        self.data.clear().write_to_json()
        for file in os.listdir(self._data_path):
            os.remove(os.path.join(self._data_path, file))


def cache_music_item(obj):
    if isinstance(obj, MusicItem):
        return {
            "__type__": "musicitem",
            "isoformat": [obj.id, obj.path, obj.params, obj.length_in_seconds]
        }
    return None


def decrypt_music_item(obj):
    if "__type__" in obj and obj["__type__"] == "musicitem":
        return MusicItem(*obj["isoformat"])
    return None
