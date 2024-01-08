from .data import User, AppData, PlayState, Singleton
from .event import ConnectionType, EventSolver, EVENT_HANDLER, DataManager, EventType
from ..constructor.elements.audio import MyAudio
from .data import Track
from .request import Sender
import flet as ft


# class LoadTrackSolver(EventSolver, metaclass=Singleton):
#     def __init__(self):
#         EVENT_HANDLER.subscribe(self, EventType.OnPlayChanged)
#
#     def notify(self, data_manager: DataManager):
#         if data_manager.connection is ConnectionType.Online:
#             if data_manager.play == PlayState.PlayFromGeneration:
#                 is_success, path, music_id = Sender.try_send_get_music_generation_request(
#                     data_manager.user.Id, data_manager.genre
#                 )
#                 if is_success:
#                     data_manager.track = Track(music_id, path)
#                 else:
#                     data_manager.play = PlayState.PauseFromGeneration
#         elif data_manager.play == PlayState.PlayFromGeneration:
#             data_manager.play = PlayState.PauseFromGeneration


class PlayTrackSolver(EventSolver, metaclass=Singleton):
    def __init__(self, page: ft.Page):
        self.page = page

        # self.existing_index = 0
        # self.existing_playlist: list[Track] = []

        self.generation_index = 0
        self.generation_playlist: list[Track] = []

        EVENT_HANDLER.subscribe(self, EventType.OnPlayChanged)

    def play_from_generation(self, data_manager: DataManager) -> None:
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
        # print('play...')
        #
        # self.page.overlay.clear()  # TODO resume
        #
        # # audio = ft.Audio(src=data_manager.track.Path, autoplay=True)
        # audio = ft.Audio(
        #     src='/Users/dimasta/work/python/pycharm/NeuroBliss/Client/Application/Cache/cd91fbd3-e155-471a-a3c2-fa29b5cdb227.wav',
        #     autoplay=False,
        #     volume=data_manager.volume / 100,
        #     balance=0,
        #     on_position_changed=self.progress_change,
        #     on_state_changed=self.check_state
        #
        # )
        #
        # self.page.overlay.append(audio)
        # self.page.update()
