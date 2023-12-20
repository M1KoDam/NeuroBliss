class Level:
    pass


class Small(Level):
    def __str__(self):
        return "small"


class Medium(Level):
    def __str__(self):
        return "medium"


class ModelLevel:
    small_model = Small
    medium_model = Medium
