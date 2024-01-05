class User:
    def __init__(self, user_id: str):
        self.user_id: str = user_id
        self.liked: list = []
        self.playlists: list[dict[str:list]] = []

