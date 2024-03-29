from ...resources import colors
from ...core.data import User, Singleton, Track
from ...core.event import \
    EventType, PageState, EventDependent, EventCaller, \
    DATA_MANAGER, DataManager, EVENT_HANDLER, PlayState, EventSolver
from ...constructor.icons import Icon, ICON
from ...core.player import PlayerSolver
from .states import VolumeStates, VolumeIconState
from .base import IconButton
from enum import Enum
from typing import Callable
import flet as ft

PAGES = [PageState.Generation, PageState.Playlist]


class AccountButton(ft.ElevatedButton, EventCaller, EventDependent, metaclass=Singleton):
    def __init__(self):
        EVENT_HANDLER.subscribe(self, EventType.OnUserChanged)

        user = DATA_MANAGER.user
        super().__init__(
            content=ft.Text(user.Login[0:2], color=ft.colors.WHITE, size=15, font_family='inter-regular'),
            bgcolor=user.AvatarColor,
            width=48,
            height=48,
            style=ft.ButtonStyle(shape={ft.MaterialState.DEFAULT: ft.CircleBorder()}, padding=10),
            on_click=lambda e: self.on_active(),
        )

    def on_active(self) -> None:
        DATA_MANAGER.page = PageState.Account

    def change_visual(self, user: User) -> None:
        self.content.value = user.Login[0:2]
        self.bgcolor = user.AvatarColor

        if DATA_MANAGER.page in PAGES:
            self.update()

    def notify(self, event: EventType, data_manager: DataManager) -> None:
        self.change_visual(data_manager.user)


class PlaylistButton(IconButton, EventCaller, EventDependent, metaclass=Singleton):
    def __init__(self):
        self.is_active = False
        EVENT_HANDLER.subscribe(self, EventType.OnPageChanged)

        super().__init__(icon=Icon.go_to_playlist, on_click=lambda e: self.on_active())

    def on_active(self) -> None:
        is_active = not self.is_active
        DATA_MANAGER.page = PageState.Playlist if is_active else PageState.Generation

    def change_visual(self, is_active: bool) -> None:
        print(type(self).__name__)

        if self.is_active == is_active:
            return

        self.is_active = is_active
        content = self.content.controls

        if self.is_active:
            content[0] = Icon.go_to_generation
        else:
            content[0] = Icon.go_to_playlist

        if DATA_MANAGER.page in PAGES:
            self.update()

    def notify(self, event: EventType, data_manager: DataManager) -> None:
        match data_manager.page:
            case PageState.Playlist:
                is_active = True
            case PageState.Generation:
                is_active = False
            case _:
                return

        self.change_visual(is_active)


class GenreButton(ft.ElevatedButton, EventCaller, EventDependent):
    def __init__(self, name: str, is_active: bool = False):
        self.genre_name = name
        self.is_active: bool = is_active
        text_color = colors.BLUE if is_active else colors.WHITE

        if is_active:
            DATA_MANAGER.genre = name

        EVENT_HANDLER.subscribe(self, EventType.OnGenresChanged)

        super().__init__(
            content=ft.Row(
                controls=[ft.Text(value=name, color=text_color, size=15, expand=True)],
                alignment=ft.MainAxisAlignment.START
            ),
            bgcolor=colors.GREY, width=110, height=48,
            on_click=lambda e: self.on_active(),
            style=ft.ButtonStyle(
                animation_duration=500,
                padding={ft.MaterialState.PRESSED: 10},
                shape={
                    ft.MaterialState.HOVERED: ft.RoundedRectangleBorder(radius=12),
                    ft.MaterialState.DEFAULT: ft.RoundedRectangleBorder(radius=8)
                }
            )
        )

    def on_active(self) -> None:
        is_active = not self.is_active

        if is_active:
            DATA_MANAGER.genre = self.genre_name
            DATA_MANAGER.play = PlayState.PlayFromGeneration
            player = PlayerSolver(None)
            player.cur_generation_index = len(player.generation_playlist) - 1
            PlayerSolver(None).play_next(DATA_MANAGER)

    def change_visual(self, is_active: bool) -> None:
        print(type(self).__name__)

        if self.is_active == is_active:
            return

        self.is_active = is_active
        button_text_area = self.content.controls[0]
        button_text_area.color = colors.BLUE if self.is_active else colors.WHITE

        if DATA_MANAGER.page == PageState.Generation:
            button_text_area.update()

    def notify(self, event: EventType, data_manager: DataManager) -> None:
        active_genres = data_manager.genre
        if self.genre_name in active_genres:
            self.change_visual(is_active=True)
        else:
            self.change_visual(is_active=False)


class PlayButtonType(Enum):
    Big = 0
    Small = 1


class PlayButton(IconButton, EventCaller, EventDependent):
    def __init__(self, button_type: PlayButtonType):
        self.is_active = False
        self.button_type = button_type

        EVENT_HANDLER.subscribe(self, EventType.OnPlayChanged)

        icon = Icon.play if button_type == PlayButtonType.Big else Icon.small_play
        super().__init__(icon=icon, on_click=lambda e: self.on_active())

    def on_active(self):
        is_active = not self.is_active

        if self.button_type == PlayButtonType.Big:
            DATA_MANAGER.play = PlayState.PlayFromGeneration if is_active else PlayState.PauseFromGeneration
        else:
            match DATA_MANAGER.play:
                case PlayState.PlayFromGeneration:
                    DATA_MANAGER.play = PlayState.PauseFromGeneration
                case PlayState.PauseFromGeneration:
                    DATA_MANAGER.play = PlayState.PlayFromGeneration
                case PlayState.PlayFromExisting:
                    DATA_MANAGER.play = PlayState.PauseFromExisting
                case PlayState.PauseFromExisting:
                    DATA_MANAGER.play = PlayState.PlayFromExisting

    def change_visual(self, is_active: bool) -> None:
        self.is_active = is_active
        content = self.content.controls

        if self.button_type == PlayButtonType.Big:
            content[0] = Icon.pause if self.is_active else Icon.play
            if DATA_MANAGER.page == PageState.Generation:
                self.update()
        else:
            content[0] = Icon.small_pause if self.is_active else Icon.small_play
            self.update()

    def notify(self, event: EventType, data_manager: DataManager) -> None:
        if self.button_type == PlayButtonType.Big:
            match data_manager.play:
                case PlayState.PlayFromGeneration:
                    self.change_visual(is_active=True)
                case PlayState.PauseFromGeneration:
                    self.change_visual(is_active=False)
                case _:
                    self.change_visual(is_active=False)
        else:
            match data_manager.play:
                case PlayState.PlayFromGeneration:
                    self.change_visual(is_active=True)
                case PlayState.PlayFromExisting:
                    self.change_visual(is_active=True)
                case _:
                    self.change_visual(is_active=False)


class PreviousTrackButton(IconButton):
    def __init__(self):
        super().__init__(icon=Icon.previous_track, on_click=lambda e: self.on_active())

    def on_active(self):
        PlayerSolver(None).play_previous(DataManager())


class NextTrackButton(IconButton):
    def __init__(self):
        super().__init__(icon=Icon.next_track, on_click=lambda e: self.on_active())

    def on_active(self):
        PlayerSolver(None).play_next(DataManager())


class LikeButton(ft.IconButton, EventDependent, EventCaller, EventSolver):
    def __init__(self, is_active=False):
        self.is_active = is_active
        icon = ICON.filled_like if self.is_active else ICON.like

        EVENT_HANDLER.subscribe(self, EventType.OnLibraryChanged)
        EVENT_HANDLER.subscribe(self, EventType.OnTrackChanged)

        super().__init__(
            content=ft.Row(controls=[icon]),
            on_click=lambda e: self.on_active())

    def on_active(self) -> None:
        if DATA_MANAGER.track is None:
            return
        is_active = not self.is_active
        if is_active:
            DATA_MANAGER.add_to_library(DATA_MANAGER.track)
        else:
            DATA_MANAGER.remove_from_library(DATA_MANAGER.track)

    def change_visual(self, is_active) -> None:
        self.is_active = is_active

        content = self.content.controls
        content[0] = ICON.filled_like if self.is_active else ICON.like

        self.update()

    def notify(self, event: EventType, data_manager: DataManager) -> None:
        if DATA_MANAGER.track in DATA_MANAGER.library and self.is_active is not True:
            self.change_visual(is_active=True)
        elif DATA_MANAGER.track not in DATA_MANAGER.library and self.is_active is True:
            self.change_visual(is_active=False)


class VolumeButton(IconButton, EventCaller, EventDependent, metaclass=Singleton):
    def __init__(self):
        self.volume_states = VolumeStates(cur_volume=DATA_MANAGER.volume)
        EVENT_HANDLER.subscribe(self, EventType.OnVolumeChanged)

        super().__init__(icon=Icon.max_volume, on_click=lambda e: self.on_active())

    def on_active(self) -> None:
        DATA_MANAGER.volume = self.volume_states.next().get_volume()

    def change_visual(self, volume: int) -> None:
        self.volume_states = VolumeStates(volume, self.volume_states.get_volume())
        content = self.content.controls

        match VolumeIconState.from_volume(self.volume_states.get_volume()):
            case VolumeIconState.Min:
                content[0] = Icon.min_volume
            case VolumeIconState.Med:
                content[0] = Icon.medium_volume
            case VolumeIconState.Max:
                content[0] = Icon.max_volume

        self.update()

    def notify(self, event: EventType, data_manager: DataManager) -> None:
        self.change_visual(data_manager.volume)


class VolumeSlider(ft.Slider, EventCaller, EventDependent, metaclass=Singleton):
    def __init__(self):
        EVENT_HANDLER.subscribe(self, EventType.OnVolumeChanged)

        super().__init__(
            min=0, max=100, width=100,
            active_color=colors.WHITE, inactive_color=colors.GREY,
            value=DATA_MANAGER.volume, on_change=lambda e: self.on_active()
        )

    def on_active(self) -> None:
        DATA_MANAGER.volume = self.value

    def change_visual(self, volume: int) -> None:
        print(type(self).__name__)

        self.value = volume
        self.update()

    def notify(self, event: EventType, data_manager: DataManager) -> None:
        self.change_visual(data_manager.volume)


class ShareButton(IconButton):
    def __init__(self):
        super().__init__(icon=ICON.share, on_click=lambda e: self.on_change())

    def on_change(self):
        print(type(self).__name__)


class TrackPositionSlider(ft.Slider, EventCaller, EventDependent, metaclass=Singleton):
    def __init__(self):
        EVENT_HANDLER.subscribe(self, EventType.OnPositionChanged)

        super().__init__(
            min=0, max=100,
            expand=True,
            active_color=colors.BLUE, inactive_color=colors.GREY,
            on_change=lambda e: self.on_active()
        )

    def on_active(self) -> None:
        ratio = self.value / self.max
        DATA_MANAGER.position_ratio = ratio

    def change_visual(self, value: float) -> None:
        self.value = value
        self.update()

    def notify(self, event: EventType, data_manager: DataManager) -> None:
        value = data_manager.position_ratio * self.max
        self.change_visual(value)


class LikeTrackItemButton(ft.IconButton, EventCaller):
    def __init__(self, on_active: Callable[[], None]):
        icon = ICON.filled_like

        super().__init__(
            content=ft.Row(controls=[icon]),
            on_click=lambda e: on_active())


class TrackItem(ft.OutlinedButton, EventDependent):
    def __init__(self, track: Track):
        self.track = track
        self.is_active = True

        EVENT_HANDLER.subscribe(self, EventType.OnTrackChanged)

        super().__init__(
            content=ft.Row(
                controls=[
                    ft.Text(
                        value=track.Name, color=colors.BLUE, size=15, font_family='inter-regular', height=20,
                        text_align=ft.TextAlign.CENTER),
                    ft.Row(controls=[ShareButton(), LikeTrackItemButton(on_active=self.on_unlike)], spacing=10)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            height=58,
            on_click=lambda e: self.on_active(),
            style=ft.ButtonStyle(
                animation_duration=500,
                padding={ft.MaterialState.PRESSED: 10},
                shape={
                    ft.MaterialState.HOVERED: ft.RoundedRectangleBorder(radius=12),
                    ft.MaterialState.DEFAULT: ft.RoundedRectangleBorder(radius=8)
                }
            )
        )

    def on_unlike(self):
        DATA_MANAGER.remove_from_library(self.track)

    def on_active(self) -> None:
        if DATA_MANAGER.track == self.track:
            match DATA_MANAGER.play:
                case PlayState.PauseFromExisting:
                    DATA_MANAGER.play = PlayState.PlayFromExisting
                case PlayState.PlayFromExisting:
                    DATA_MANAGER.play = PlayState.PauseFromExisting
                case PlayState.PlayFromGeneration:
                    DATA_MANAGER.play = PlayState.PlayFromExisting
                case PlayState.PauseFromGeneration:
                    DATA_MANAGER.play = PlayState.PauseFromExisting
        else:
            DATA_MANAGER.track = self.track
            DATA_MANAGER.play = PlayState.PlayFromExisting

    def change_visual(self, is_active: bool) -> None:
        color = colors.BLUE if is_active else colors.WHITE

        text = self.content.controls[0]
        text.color = color
        if DATA_MANAGER.page == PageState.Playlist and self.track in DATA_MANAGER.library:
            text.update()

    def notify(self, event: EventType, data_manager: 'DataManager') -> None:
        if data_manager.track == self.track:
            self.change_visual(is_active=True)
        else:
            self.change_visual(is_active=False)
