import os
from EasyToCacheLib.easy_to_cache import Cache
from Server.Domain.music_item import MusicItem


class MusicRepository:
    def __init__(self, cache_path, data_path):
        self.cache_path = cache_path
        self.data_path = data_path
        self.cache = Cache(cache_path + "music.json", True).set_json_handlers(decrypt_music_item, cache_music_item)

    def add_music(self, music_item: MusicItem):
        self.cache.add(music_item.id, music_item).write_to_json()

    def get_music_by_id(self, music_id) -> MusicItem:
        return self.cache.try_get(music_id)

    def delete_music_by_id(self, music_id):
        if self.cache.try_get(music_id):
            self.cache.remove(music_id).write_to_json()
            os.remove(os.path.join(self.data_path, os.path.join(self.data_path, f"{music_id}.wav")))

    def clear(self):
        self.cache.clear().write_to_json()
        for file in os.listdir(self.data_path):
            os.remove(os.path.join(self.data_path, file))


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
