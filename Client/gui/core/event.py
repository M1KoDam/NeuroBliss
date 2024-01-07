from .data import AppData, PlayState, PageState, Track, User, ConnectionType, Singleton
from typing import Protocol, Any
from enum import Enum


class EventType(Enum):
    OnVolumeChanged = 0
    OnPlayChanged = 1
    OnTrackChanged = 2
    OnGenresChanged = 3
    OnPageChanged = 4
    OnUserChanged = 5
    OnConnectionChanged = 6


class OnClickHandle(Protocol):
    @staticmethod
    def __call__(event: Any) -> None:
        ...


class EventSolver:
    """Event solver can't be the cause of the event, but should solve it"""

    def notify(self, data_manager: 'DataManager') -> None:
        """Describes how to solve event"""
        ...


class EventCaller:
    """Event caller may be the cause of the event.
    It doesn't solve event and don't change its appearance according to event"""

    def on_active(self) -> None:
        """Says what to do data manager"""
        ...


class EventDependent:
    """Event dependent doesn't solve event, be the cause of it, but change self appearance according to event"""

    def change_visual(self, arg: Any) -> None:
        """Sets internal arguments to those given in 'args'. Changes its visual appearance"""
        ...

    def notify(self, data_manager: 'DataManager') -> None:
        """Describes what to do when this object is notified that it needs to change according to application data"""
        ...


class DataManager(metaclass=Singleton):
    def __init__(self):
        self.app_data = AppData()

    @property
    def play(self) -> PlayState:
        return self.app_data.Play

    @play.setter
    def play(self, new_state: PlayState) -> None:
        self.app_data.Play = new_state
        self.raise_event(EventType.OnPlayChanged)

    @property
    def track(self) -> Track:
        return self.app_data.Track

    @track.setter
    def track(self, new_track: Track) -> None:
        self.app_data.Track = new_track
        self.raise_event(EventType.OnTrackChanged)

    @property
    def volume(self) -> int:
        return self.app_data.Volume

    @volume.setter
    def volume(self, new_volume: int) -> None:
        self.app_data.Volume = new_volume
        self.raise_event(EventType.OnVolumeChanged)

    @property
    def genre(self) -> str:
        return self.app_data.ActiveGenre

    @genre.setter
    def genre(self, new_genre: str) -> None:
        self.app_data.ActiveGenre = new_genre
        self.raise_event(EventType.OnGenresChanged)

    @property
    def page(self) -> PageState:
        return self.app_data.Page

    @page.setter
    def page(self, new_page: PageState) -> None:
        self.app_data.Page = new_page
        self.raise_event(EventType.OnPageChanged)

    @property
    def user(self) -> User:
        return self.app_data.User

    @user.setter
    def user(self, new_user: User) -> None:
        self.app_data.User = new_user
        self.raise_event(EventType.OnUserChanged)

    @property
    def connection(self) -> ConnectionType:
        return self.app_data.Connection

    @connection.setter
    def connection(self, new_connection: ConnectionType) -> None:
        self.app_data.Connection = new_connection
        self.raise_event(EventType.OnConnectionChanged)

    @staticmethod
    def raise_event(event_type: EventType) -> None:
        EVENT_HANDLER.handle_event(event_type)


class EventHandler(metaclass=Singleton):
    def __init__(self):
        self.dependents: list[tuple[EventType, EventDependent]] = []
        self.solvers: list[tuple[EventType, EventSolver]] = []

    def subscribe(self, sub: EventDependent | EventSolver, event_type: EventType) -> None:
        if isinstance(sub, EventDependent):
            self.dependents.append((event_type, sub))
        elif isinstance(sub, EventSolver):
            self.solvers.append((event_type, sub))
        else:
            raise ValueError

    def handle_event(self, current_event: EventType) -> None:
        for event, solver in self.solvers:
            if current_event == event:
                solver.notify(DATA_MANAGER)

        for event, dependent in self.dependents:
            if current_event == event:
                dependent.notify(DATA_MANAGER)


EVENT_HANDLER = EventHandler()
DATA_MANAGER = DataManager()
