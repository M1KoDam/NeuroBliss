class User:
    def __init__(self, user_id: str, liked: list = None, playlists: list = None):
        self.user_id: str = user_id

        self.liked: list = []
        if liked is not None:
            self.liked = liked

        self.playlists: list[dict[str:list]] = []
        if playlists is not None:
            self.playlists = playlists
