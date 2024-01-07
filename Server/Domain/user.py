
class User:
    __created_users = {}

    def __init__(self, user_id: str, liked: list = None, playlists: list = None):
        self.user_id: str = user_id

        self.liked: list = []
        if liked is not None:
            self.liked = liked

        self.playlists: list[dict[str:list]] = []
        if playlists is not None:
            self.playlists = playlists

    def add_music_to_liked(self, music_id: str):
        self.liked.append(music_id)

    def __new__(cls, *args, **kwargs):
        if args[0] in cls.__created_users.keys():
            return cls.__created_users[args[0]]
        new_user = super().__new__(cls)
        cls.__created_users[args[0]] = new_user
        return new_user


if __name__ == '__main__':
    user = User("jewfwef0")
