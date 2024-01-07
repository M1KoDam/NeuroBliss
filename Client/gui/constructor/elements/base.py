from ...resources import colors
from ...core.request import Sender
from ...core.data import User, ConnectionType, Singleton
from ...core.event import OnClickHandle, EventCaller, DATA_MANAGER
from ...constructor.icons import Icon
from .color_picker import ColorPicker
from typing import Callable
import flet as ft
from Client.Application.client_api import register_user
import httpx


class IconButton(ft.IconButton):
    def __init__(self, icon: Icon, on_click: OnClickHandle):
        super().__init__(
            content=ft.Row(controls=[icon]),
            on_click=on_click
        )


class TextButton(ft.TextButton):
    def __init__(self, text: str, icon: Icon, on_click: OnClickHandle):
        super().__init__(
            content=ft.Row(
                controls=[
                    icon, ft.Text(value=text, color=ft.colors.WHITE, size=15, font_family='inter-regular')
                ],
                alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            on_click=on_click
        )


class TextField(ft.TextField):
    def __init__(self, label: str):
        super().__init__(
            label=label,
            color=colors.BLUE,
            focused_color=ft.colors.WHITE,
            focused_border_color=ft.colors.WHITE,
            border_color=ft.colors.GREY,
            cursor_color=ft.colors.WHITE,
            expand=True,
            height=50
        )


class LoginField(TextField, metaclass=Singleton):
    def __init__(self):
        super().__init__(label="login")


class PasswordField(TextField, metaclass=Singleton):
    def __init__(self):
        super().__init__(label="password")


class CustomColorPicker(ColorPicker, metaclass=Singleton):
    def __init__(self):
        super().__init__(
            base_color=colors.LIGHT_GREY,
            map_width=380,
        )


class UploadButton(ft.ElevatedButton, EventCaller):
    def __init__(
        self,
        label: str,
        width: int,
        on_close: Callable[[bool], None] = None,
        on_server_unreachable: Callable[[], None] = None
    ):
        self.on_close = on_close
        self.on_server_unreachable = on_server_unreachable

        super().__init__(
            content=ft.Row(
                controls=[ft.Text(value=label, color=ft.colors.WHITE, size=15, expand=True)],
                alignment=ft.MainAxisAlignment.START
            ),
            bgcolor=colors.GREY, width=width, height=40,
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
        need_to_close = True

        login = LoginField().value
        if not login:
            LoginField().error_text = "login cannot be blank"
            LoginField().update()
            need_to_close = False

        password = PasswordField().value
        if not password:
            PasswordField().error_text = "password cannot be blank"
            PasswordField().update()
            need_to_close = False

        avatar_color = CustomColorPicker().color
        if not avatar_color:
            avatar_color = DATA_MANAGER.user.AvatarColor

        user_id = None
        if self.on_close is not None:
            if need_to_close:
                is_success, user_id = Sender.try_make_registration_request(login, password)

            self.on_close(need_to_close)

        if need_to_close:
            LoginField().error_text = ""
            LoginField().update()
            PasswordField().error_text = ""
            PasswordField().update()
            if DATA_MANAGER.connection == ConnectionType.Online:
                DATA_MANAGER.user = User(
                    Login=login, Password=password, AvatarColor=avatar_color,
                    OriginalLogin=login, OriginalPassword=password, Id=user_id
                )
            else:
                DATA_MANAGER.user = User(
                    Login=login, Password=password, AvatarColor=avatar_color,
                    OriginalLogin=None, OriginalPassword=None, Id=None
                )


class SettingListView(ft.ListView):
    def __init__(self, label: str | None):
        controls = [ft.Text(value=label, color=ft.colors.WHITE, size=15, expand=True)] if label is not None else []
        controls.extend(
            (LoginField(),
             PasswordField(),
             CustomColorPicker())
        )

        super().__init__(
            controls=controls,
            spacing=10,
            expand=True
        )
