class MusicItem:
    __created_music = {}

    def __init__(self, music_id: str, path: str, phrase: str, length_in_seconds: int, is_ready=False):
        self.id: str = music_id
        self.path: str = path
        self.phrase: str = phrase
        self.length_in_seconds: int = length_in_seconds
        self.is_ready: bool = is_ready

    def change_path(self, new_path):
        self.path = new_path
        return self

    def copy(self):
        return MusicItem(self.id, self.path, self.phrase, self.length_in_seconds, self.is_ready)

    def __new__(cls, *args, **kwargs):
        if args[0] in cls.__created_music.keys():
            return cls.__created_music[args[0]]
        new_user = super().__new__(cls)
        cls.__created_music[args[0]] = new_user
        return new_user
