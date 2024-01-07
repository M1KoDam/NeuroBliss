from ..resources import colors
from dataclasses import dataclass
from enum import Enum


class Singleton(type):
    instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls.instances:
            cls.instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls.instances[cls]


class PlayState(Enum):
    PlayFromGeneration = 0
    PauseFromGeneration = 1
    PlayFromExisting = 2
    PauseFromExisting = 3

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.__str__()


class DummyTrack:
    ...


@dataclass
class User:
    Login: str = '?'
    Password: str = ''
    AvatarColor: str = colors.LIGHT_GREY
    Id: str = ''


class PageState(Enum):
    Generation = '/'
    Playlist = '/playlist'
    Account = '/account'
    Search = '/account/search'
    Settings = '/account/settings'

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.__str__()


class AppData(metaclass=Singleton):
    Play: PlayState = PlayState.PauseFromGeneration
    Track: DummyTrack = None
    Page: PageState = PageState.Generation
    ActiveGenres: set[str] = set()
    Volume: int = 100
    User: User = User()

    def __str__(self) -> str:
        parts = [
            type(self).__name__,
            '(', f'{self.Play=}, ', f'{self.Track=}, ', f'{self.Page=}, ',
            f'{self.ActiveGenres=}, ', f'{self.Volume=}, ', f'{self.User=}', ')'
        ]
        return ''.join(parts)

    def __repr__(self) -> str:
        return self.__str__()


APP_DATA = AppData()
