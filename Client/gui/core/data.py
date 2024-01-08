from ..resources import colors
from dataclasses import dataclass
from enum import Enum
import flet as ft


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


@dataclass
class Track:
    Name: str = None
    Path: str = None
    Audio: ft.Audio = None

    def __hash__(self):
        return hash((self.Name, self.Path))

    def __eq__(self, other):
        if isinstance(other, Track):
            return (self.Name, self.Path) == (other.Name, other.Path)
        return False


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


class AppData:
    Connection = ConnectionType.Offline
    Play: PlayState = PlayState.PauseFromGeneration
    Track: Track = None
    Page: PageState = PageState.Generation
    ActiveGenre: str = None
    Volume: float = 100
    User: User = User()
    Library: set[Track] = set()

    def __str__(self) -> str:
        parts = [
            type(self).__name__,
            '(', f'{self.Connection=}, 'f'{self.Play=}, ', f'{self.Track=}, ', f'{self.Page=}, ',
            f'{self.ActiveGenre=}, ', f'{self.Volume=}, ', f'{self.User=}', f'{self.Library=}', ')'
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
