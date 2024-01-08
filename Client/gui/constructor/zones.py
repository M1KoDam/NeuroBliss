from ..resources import colors
from ..core.data import ConnectionType, Singleton
from ..core.event import EventSolver, EVENT_HANDLER, EventType, DataManager
from .elements.for_generation_playlist_pages import \
    GenreButton, PlayButton, PlaylistButton, PlayButtonType, PreviousTrackButton, \
    NextTrackButton, LikeButton, ShareButton, VolumeButton, VolumeSlider, AccountButton
from .elements.for_account_pages import \
    UserAvatar, UserName, SearchButton, SettingsButton, SmallGenerationButton, \
    SmallPlaylistButton, SearchRow, SettingsColumn
from .elements.for_registrate import RegistrateColumn
from .elements.base import UploadButton, SingInButton
import flet as ft


class PlaylistArea(ft.Card, metaclass=Singleton):
    def __init__(self):
        super().__init__(
            content=ft.Row(
                controls=[
                ],
                alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True,
            ),
            color=colors.DARK_SLATE_BLUE,
            expand=True,
        )


class MoodGrid(ft.Column, metaclass=Singleton):
    def __init__(self):
        super().__init__(
            controls=[
                ft.Row(
                    controls=[
                        GenreButton('Angry'), GenreButton('Happy'), GenreButton('Dark'), GenreButton('Sentimental')
                    ],
                    spacing=37
                ),
                ft.Row(
                    controls=[
                        GenreButton('Romantic'), GenreButton('Sad'), GenreButton('Dreamy'), GenreButton('My steroid')
                    ],
                    spacing=37
                )
            ],
            spacing=34,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )


class GenerationArea(ft.Card, metaclass=Singleton):
    def __init__(self):
        super().__init__(
            content=ft.Row(
                controls=[
                    PlayButton(PlayButtonType.Big),
                    MoodGrid(),
                ],
                alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True,
            ),
            color=colors.DARK_SLATE_BLUE,
            expand=True,
        )


class TopBar(ft.Row, metaclass=Singleton):
    def __init__(self):
        super().__init__(
            controls=[
                PlaylistButton(),
                AccountButton(),
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            height=48,
        )


class BottomBar(ft.Row, metaclass=Singleton):
    def __init__(self):
        super().__init__(
            controls=[
                PreviousTrackButton(), PlayButton(PlayButtonType.Small), NextTrackButton(),
                ft.Slider(min=0, max=100, expand=True, active_color=colors.BLUE, inactive_color=colors.GREY),
                LikeButton(), ShareButton(), ft.Row(controls=[VolumeButton(), VolumeSlider()], spacing=0)
            ],
            spacing=24,
            height=50,
        )


class UserBar(ft.Row, metaclass=Singleton):
    def __init__(self):
        super().__init__(
            controls=[
                UserAvatar(),
                ft.Row(controls=[UserName()], alignment=ft.MainAxisAlignment.CENTER, expand=True)
            ],
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            height=100,
        )


class NavigationBar(ft.Card, metaclass=Singleton):
    def __init__(self):
        super().__init__(
            content=ft.Column(
                controls=[
                    SearchButton(),
                    SmallGenerationButton(),
                    SmallPlaylistButton(),
                    SettingsButton(),
                ],
                alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                horizontal_alignment=ft.CrossAxisAlignment.START,
                expand=True
            ),
            color=colors.DARK_SLATE_BLUE,
            width=150,
        )


class DefaultArea(ft.Card, metaclass=Singleton):
    def __init__(self):
        super().__init__(
            content=ft.Column(
                controls=[
                    ft.Text('select page', color=ft.colors.GREY, size=15, font_family='inter-light'),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True
            ),
            color=colors.DARK_SLATE_BLUE,
            expand=True,
        )


class SearchArea(ft.Card, metaclass=Singleton):
    def __init__(self):
        super().__init__(
            content=ft.Stack(
                controls=[
                    SearchRow(),
                ],
                expand=True
            ),
            color=colors.DARK_SLATE_BLUE,
            expand=True,
        )


class SettingsArea(ft.Card, metaclass=Singleton):
    def __init__(self):
        super().__init__(
            content=ft.Stack(
                controls=[
                    SettingsColumn(),
                ],
                expand=True
            ),
            color=colors.DARK_SLATE_BLUE,
            expand=True,
        )


class RegistrateArea(ft.Card, metaclass=Singleton):
    def __init__(self):
        super().__init__(
            content=ft.Stack(
                controls=[
                    RegistrateColumn(),
                ],
                expand=True
            ),
            color=colors.DARK_SLATE_BLUE,
            width=625, height=300,
        )


class Dialog(ft.AlertDialog, metaclass=Singleton):
    def __init__(self, need_to_call_dialog: bool):
        super().__init__(
            open=need_to_call_dialog,
            modal=True,
            title=ft.Text("Welcome!"),
            content=RegistrateArea(),
            actions=[
                SingInButton(on_close=self.on_close),
                UploadButton(label='Sign up', width=74, on_close=self.on_close)
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

    def on_close(self, need_to_close: bool):
        if need_to_close:
            self.open = False
            self.update()


class ServerUnreachableBanner(ft.Banner, EventSolver, metaclass=Singleton):
    def __init__(self, page: ft.Page):
        self.page = page
        page.banner = self

        EVENT_HANDLER.subscribe(self, EventType.OnConnectionChanged)

        super().__init__(
            bgcolor=ft.colors.AMBER_100,
            leading=ft.Icon(ft.icons.WARNING_AMBER_ROUNDED, color=ft.colors.AMBER, size=40),
            content=ft.Text(
                value="oops, server is unreachable", color=ft.colors.BLACK, size=20, font_family='inter-regular'
            ),
            actions=[
                ft.TextButton(
                    content=ft.Text(
                        value="close app", color=ft.colors.BLUE, size=20, font_family='inter-regular'
                        ),
                    on_click=lambda e: self.close_app()
                )
            ]
        )

    def notify(self, data_manager: DataManager) -> None:
        if data_manager.connection == ConnectionType.Offline:
            self.invoke()

    def invoke(self):
        self.open = True
        Dialog(need_to_call_dialog=False)
        if self.page:
            self.page.update()

    def close_app(self):
        self.page.window_close()
