import os
from EasyToCacheLib.easy_to_cache import Cache
from Server.Domain.music_item import MusicItem


class ClientRepository:
    __instance = None

    def __init__(self, data_path):
        if self.__initialized:
            return
        self.__initialized = True

        print("INIT ClientRepository")
        self.data_path = data_path
        self.data = Cache(data_path + "data.json", True, decrypt_music_item, cache_music_item)

    def add_music(self, music_item: MusicItem):
        self.data.add(music_item.id, music_item).write_to_json()

    def get_music_by_id(self, music_id) -> MusicItem:
        return self.data.try_get(music_id)

    def delete_music_by_id(self, music_id):
        if self.data.try_get(music_id):
            self.data.remove(music_id).write_to_json()
            os.remove(os.path.join(self.data_path, os.path.join(self.data_path, f"{music_id}.wav")))

    def clear(self):
        self.data.clear().write_to_json()
        for file in os.listdir(self.data_path):
            os.remove(os.path.join(self.data_path, file))

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__initialized = False
        return cls.__instance


def cache_music_item(obj):
    if isinstance(obj, MusicItem):
        return {
            "__type__": "musicitem",
            "isoformat": [obj.id, obj.path, obj.phrase, obj.length_in_seconds, obj.is_ready]
        }
    return None


def decrypt_music_item(obj):
    if "__type__" in obj and obj["__type__"] == "musicitem":
        return MusicItem(*obj["isoformat"])
    return None
