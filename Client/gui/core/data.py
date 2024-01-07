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
    Password: str = None
    AvatarColor: str = colors.LIGHT_GREY
    OriginalLogin: str = None
    OriginalPassword: str = None
    Id: str = None


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


class ConnectionType(Enum):
    Offline = 0
    Online = 1

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.__str__()


class AppData(metaclass=Singleton):
    Connection = ConnectionType.Offline
    Play: PlayState = PlayState.PauseFromGeneration
    Track: DummyTrack = None
    Page: PageState = PageState.Generation
    ActiveGenres: set[str] = set()
    Volume: int = 100
    User: User = User()

    def __str__(self) -> str:
        parts = [
            type(self).__name__,
            '(', f'{self.Connection=}, 'f'{self.Play=}, ', f'{self.Track=}, ', f'{self.Page=}, ',
            f'{self.ActiveGenres=}, ', f'{self.Volume=}, ', f'{self.User=}', ')'
        ]
        return ''.join(parts)

    def __repr__(self) -> str:
        return self.__str__()

    def get_user_info(self) -> list[str]:
        return [
            f'Login={str(self.User.Login)}',
            f'Password={str(self.User.Password)}',
            f'AvatarColor={str(self.User.AvatarColor)}',
            f'OriginalLogin={str(self.User.OriginalLogin)}',
            f'OriginalPassword={str(self.User.OriginalPassword)}',
            f'Id={str(self.User.Id)}',
        ]
