from .data import User, AppData, PlayState, Singleton
from .event import ConnectionType, EventSolver, EVENT_HANDLER, DataManager, EventType
from .data import Track
from .request import Sender
import flet as ft


class LoadTrackSolver(EventSolver, metaclass=Singleton):
    def __init__(self):
        EVENT_HANDLER.subscribe(self, EventType.OnPlayChanged)

    def notify(self, data_manager: DataManager):
        if data_manager.connection is ConnectionType.Online:
            if data_manager.play == PlayState.PlayFromGeneration:
                is_success, path, music_id = Sender.try_send_get_music_generation_request(
                    data_manager.user.Id, data_manager.genre
                )
                if is_success:
                    data_manager.track = Track(music_id, path)
                else:
                    data_manager.play = PlayState.PauseFromGeneration
        elif data_manager.play == PlayState.PlayFromGeneration:
            data_manager.play = PlayState.PauseFromGeneration


class PlayTrackSolver(EventSolver, metaclass=Singleton):
    def __init__(self):
        EVENT_HANDLER.subscribe(self, EventType.OnTrackChanged)

    def notify(self, data_manager: DataManager):
        print('lol:)')

        audio1 = ft.Audio(
            src=data_manager.track.Path, autoplay=True
        )
