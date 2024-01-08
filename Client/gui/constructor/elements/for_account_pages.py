from ...core.data import User, Singleton
from ...core.event import \
    EventType, PageState, EventDependent, \
    EventCaller, DATA_MANAGER, DataManager, EVENT_HANDLER
from ...constructor.icons import Icon
from .base import TextButton, TextField, SettingListView, UploadButton
import flet as ft


class UserAvatar(ft.CircleAvatar, EventDependent, metaclass=Singleton):
    def __init__(self):
        EVENT_HANDLER.subscribe(self, EventType.OnUserChanged)

        user = DATA_MANAGER.user
        super().__init__(
            radius=48,
            content=ft.Text(value=user.Login[0:2], color=ft.colors.WHITE, size=30, font_family='inter-regular'),
            color=ft.colors.WHITE,
            bgcolor=user.AvatarColor,
        )

    def change_visual(self, user: User) -> None:
        self.content.value = user.Login[0:2]
        self.bgcolor = user.AvatarColor

        if DATA_MANAGER.page in [PageState.Account, PageState.Settings, PageState.Search]:
            self.update()

    def notify(self, event: EventType, data_manager: DataManager) -> None:
        self.change_visual(data_manager.user)


class UserName(ft.Text, EventDependent, metaclass=Singleton):
    def __init__(self):
        EVENT_HANDLER.subscribe(self, EventType.OnUserChanged)

        super().__init__(
            value=DATA_MANAGER.user.Login, color=ft.colors.WHITE, size=30, font_family='inter-regular'
        )

    def change_visual(self, login: str) -> None:
        self.value = login

        if DATA_MANAGER.page in [PageState.Account, PageState.Settings, PageState.Search]:
            self.update()

    def notify(self, event: EventType, data_manager: DataManager) -> None:
        self.change_visual(data_manager.user.Login)


class SearchButton(TextButton, EventCaller, metaclass=Singleton):
    def __init__(self):
        super().__init__(text='search', icon=Icon.search, on_click=lambda e: self.on_active())

    def on_active(self) -> None:
        DATA_MANAGER.page = PageState.Search


class SettingsButton(TextButton, EventCaller, metaclass=Singleton):
    def __init__(self):
        super().__init__(text='settings', icon=Icon.settings, on_click=lambda e: self.on_active())

    def on_active(self) -> None:
        DATA_MANAGER.page = PageState.Settings


class SmallPlaylistButton(TextButton, EventCaller, metaclass=Singleton):
    def __init__(self):
        super().__init__(text='playlist', icon=Icon.small_go_to_playlist, on_click=lambda e: self.on_active())

    def on_active(self) -> None:
        DATA_MANAGER.page = PageState.Playlist


class SmallGenerationButton(TextButton, EventCaller, metaclass=Singleton):
    def __init__(self):
        super().__init__(text='generation', icon=Icon.small_go_to_generation, on_click=lambda e: self.on_active())

    def on_active(self) -> None:
        DATA_MANAGER.page = PageState.Generation


class SearchField(TextField, metaclass=Singleton):
    def __init__(self):
        super().__init__(label="track id")


class SearchRow(ft.Row, metaclass=Singleton):
    def __init__(self):
        super().__init__(
            controls=[
                Icon.search,
                SearchField()
            ],
            top=10,
            left=10,
            right=10,
            height=50
        )


class SettingsColumn(ft.Column, metaclass=Singleton):
    def __init__(self):
        super().__init__(
            controls=[
                SettingListView(label='New settings:'),
                UploadButton(label='upload new settings', width=170)
            ],
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            spacing=10,
            top=10,
            left=10,
            right=10,
            bottom=10,
            height=300,
        )
