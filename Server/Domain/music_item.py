import uuid


class MusicItem:
    def __init__(self, music_id, path, params, length_in_seconds):
        self.id = music_id
        self.path = path
        self.params = params
        self.length_in_seconds = length_in_seconds
