from ...resources import colors
from ...core.data import User, Singleton
from ...core.event import OnClickHandle, EventCaller, DATA_MANAGER
from ...constructor.icons import Icon
from .color_picker import ColorPicker
from typing import Callable
import flet as ft
from Client.Application.client_api import register_user


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
            base_color='#ffffff',
            map_width=380,
        )


class UploadButton(ft.ElevatedButton, EventCaller):
    def __init__(self, label: str, width: int, additive_func: Callable[[bool], None] = None):
        self.additive_func = additive_func
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

        if self.additive_func is not None:
            register_item = register_user(login=login, password=password)
            message = register_item["message"]
            user_id = None
            if message:
                user_id = register_item["id"]

            need_to_close = message
            self.additive_func(need_to_close)

        if need_to_close:
            LoginField().error_text = ""
            LoginField().update()
            PasswordField().error_text = ""
            PasswordField().update()
            DATA_MANAGER.user = User(Login=login, Password=password, AvatarColor=avatar_color)


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