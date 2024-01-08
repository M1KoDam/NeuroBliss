from .data import PlayState, Singleton
from .event import EventSolver, EVENT_HANDLER, DataManager, EventType
from ..constructor.elements.audio import MyAudio
from .data import Track
from .request import Sender
import flet as ft


class PlayerSolver(EventSolver, metaclass=Singleton):
    def __init__(self, page: ft.Page):
        self.page = page

        # self.existing_index = 0
        # self.existing_playlist: list[Track] = []

        self.generation_index = 0
        self.generation_playlist: list[Track] = []

        EVENT_HANDLER.subscribe(self, EventType.OnPlayChanged)

    def play_from_generation(self, data_manager: DataManager) -> None:
        if data_manager.play == PlayState.PauseFromGeneration:
            data_manager.play = PlayState.PlayFromGeneration
        if self.generation_index == len(self.generation_playlist):
            is_success, path, music_id = Sender.try_send_get_music_generation_request(
                data_manager.user.Id, data_manager.genre
            )
            if is_success:
                audio = MyAudio(
                    path=path,
                    check_state=self.check_state
                )
                track = Track(Name=music_id, Path=path, Audio=audio)
                self.generation_playlist.append(Track(Name=music_id, Path=path, Audio=audio))
                data_manager.track = self.generation_playlist[self.generation_index]
                self.page.overlay.append(audio)
                self.page.update()
                data_manager.track = track
            else:
                data_manager.play = PlayState.PauseFromGeneration
        else:
            self.generation_playlist[self.generation_index].Audio.resume()
            data_manager.track = self.generation_playlist[self.generation_index]

    def pause_from_generation(self) -> None:
        self.generation_playlist[self.generation_index].Audio.pause()

    def check_state(self, e):
        if e.data == "completed":
            if DataManager().play == PlayState.PlayFromGeneration:
                self.generation_index += 1
                self.play_from_generation(DataManager())
            elif DataManager().play == PlayState.PlayFromExisting:
                ...

    def play_next(self):
        data_manager = DataManager()

        if data_manager.play == PlayState.PlayFromGeneration or data_manager.play == PlayState.PauseFromGeneration:
            self.generation_index = min(self.generation_index + 1, len(self.generation_playlist))
            if 0 <= self.generation_index - 1 < len(self.generation_playlist):
                self.generation_playlist[self.generation_index - 1].Audio.pause()
            self.play_from_generation(data_manager)
        else:
            ...

    def play_previous(self):
        data_manager = DataManager()

        if data_manager.play == PlayState.PlayFromGeneration or data_manager.play == PlayState.PauseFromGeneration:
            if self.generation_index - 1 < 0 or self.generation_index == 0 and len(self.generation_playlist) == 0:
                self.play_next()
            else:
                self.generation_index -= 1
                if 0 <= self.generation_index + 1 < len(self.generation_playlist):
                    self.generation_playlist[self.generation_index + 1].Audio.pause()
                DataManager.track = self.generation_playlist[self.generation_index]
                self.generation_playlist[self.generation_index].Audio.play()
        else:
            ...

    def notify(self, event: EventType, data_manager: DataManager):
        match data_manager.play:
            case PlayState.PlayFromGeneration:
                self.play_from_generation(data_manager)
            case PlayState.PlayFromExisting:
                ...
            case PlayState.PauseFromGeneration:
                self.pause_from_generation()
            case PlayState.PauseFromExisting:
                ...
