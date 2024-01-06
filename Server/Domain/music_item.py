class MusicItem:
    def __init__(self, music_id, path, params, length_in_seconds, is_ready=False):
        self.id = music_id
        self.path = path
        self.params = params
        self.length_in_seconds = length_in_seconds
        self.is_ready = is_ready

    def change_path(self, new_path):
        self.path = new_path
        return self

    def copy(self):
        return MusicItem(self.id, self.path, self.params, self.length_in_seconds, self.is_ready)


