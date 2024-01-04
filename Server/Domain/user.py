class User:
    def __init__(self, user_id, nickname, hashed_password):
        self.user_id = user_id
        self.nickname = nickname
        self.hashed_password = hashed_password
