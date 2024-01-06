from ...core.data import Singleton
from .base import SettingListView
import flet as ft


class RegistrateColumn(ft.Column, metaclass=Singleton):
    def __init__(self):
        super().__init__(
            controls=[
                SettingListView(label='New settings:'),
            ],
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            spacing=10,
            top=10,
            left=10,
            right=10,
            bottom=10,
            height=300,
        )
