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

        self.cur_generation_index = None
        self.generation_playlist: list[Track] = []

        EVENT_HANDLER.subscribe(self, EventType.OnPlayChanged)

    def generate_new(self, data_manager: DataManager) -> None:
        is_success, path, music_id = Sender.try_send_get_music_generation_request(
            data_manager.user.Id, data_manager.genre
        )
        if is_success:
            audio = MyAudio(
                path=path,
                check_state=self.check_state
            )
            self.cur_generation_index = len(self.generation_playlist)

            if 0 <= self.cur_generation_index - 1 <= len(self.generation_playlist):
                self.generation_playlist[self.cur_generation_index - 1].Audio.pause()

            track = Track(Name=music_id, Path=path, Audio=audio)
            self.generation_playlist.append(Track(Name=music_id, Path=path, Audio=audio))
            data_manager.track = track

            self.page.overlay.append(audio)
            self.page.update()
        else:
            data_manager.play = PlayState.PauseFromGeneration

    def check_state(self, e):
        if e.data == "completed":
            if DataManager().play == PlayState.PlayFromGeneration:
                self.play_next(DataManager())
            elif DataManager().play == PlayState.PlayFromExisting:
                ...

    def play_from_generation(self, data_manager: DataManager) -> None:
        if self.cur_generation_index is None:
            self.play_next(data_manager)
        else:
            self.generation_playlist[self.cur_generation_index].Audio.resume()
            data_manager.track = self.generation_playlist[self.cur_generation_index]

    def pause_from_generation(self, data_manager: DataManager) -> None:
        if self.cur_generation_index is not None:
            self.generation_playlist[self.cur_generation_index].Audio.pause()

    def play_next(self, data_manager: DataManager):
        if data_manager.play == PlayState.PauseFromGeneration:
            data_manager.play = PlayState.PlayFromGeneration
        if self.cur_generation_index is None or self.cur_generation_index == len(self.generation_playlist) - 1:
            self.generate_new(data_manager)
        else:
            self.generation_playlist[self.cur_generation_index].Audio.pause()
            self.cur_generation_index += 1
            track = self.generation_playlist[self.cur_generation_index]
            track.Audio.play()
            data_manager.track = track

        print(self.cur_generation_index, len(self.generation_playlist))

    def play_previous(self, data_manager: DataManager):
        if data_manager.play == PlayState.PlayFromGeneration or data_manager.play == PlayState.PauseFromGeneration:
            data_manager.play = PlayState.PlayFromGeneration
        if self.cur_generation_index is None or self.cur_generation_index == 0:
            if self.cur_generation_index is not None:
                self.generation_playlist[self.cur_generation_index].Audio.pause()
            self.generate_new(data_manager)
        else:
            self.generation_playlist[self.cur_generation_index].Audio.pause()
            self.cur_generation_index -= 1
            track = self.generation_playlist[self.cur_generation_index]
            track.Audio.play()
            data_manager.track = track

        print(self.cur_generation_index, len(self.generation_playlist))

    def notify(self, event: EventType, data_manager: DataManager):
        match data_manager.play:
            case PlayState.PlayFromGeneration:
                self.play_from_generation(data_manager)
            case PlayState.PlayFromExisting:
                ...
            case PlayState.PauseFromGeneration:
                self.pause_from_generation(data_manager)
            case PlayState.PauseFromExisting:
                ...
