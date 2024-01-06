from gui.resources import colors, fonts, ASSETS_PATH
from gui.core.data import Singleton
from gui.core.event import \
    EventType, PageState, EventSolver, DATA_MANAGER, \
    DataManager, EVENT_HANDLER
from gui.constructor.zones import \
    TopBar, GenerationArea, PlaylistArea, BottomBar, \
    UserBar, NavigationBar, DefaultArea, SearchArea, SettingsArea, Dialog
import flet as ft


def set_up_page_appearance(page: ft.Page) -> None:
    def page_resize():
        print(f"{page.width} x {page.height}")
        print(DATA_MANAGER.app_data)

    page.title = 'Neiro Bliss'
    page.fonts = {
        'inter-light': fonts.INTER_LIGHT,
        'inter-medium': fonts.INTER_MEDIUM,
        'inter-regular': fonts.INTER_REGULAR,
    }
    page.dark_theme = ft.theme.Theme(color_scheme_seed=colors.DODGER_BLUE, font_family='inter-regular')
    page.theme_mode = ft.ThemeMode.DARK

    page.window_width = 840
    page.window_height = 600

    page.window_min_width = 800
    page.window_min_height = 400

    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    page.bgcolor = colors.DARK_GREY
    page.window_resizable = True

    page.on_resize = lambda e: page_resize()
    page.update()


class Router(EventSolver, metaclass=Singleton):
    def __init__(self, page: ft.Page):
        self.page = page

        self.routes = {
            PageState.Generation: (
                TopBar(),
                GenerationArea(),
                BottomBar(),
            ),
            PageState.Playlist: (
                TopBar(),
                PlaylistArea(),
                BottomBar(),
            ),
            PageState.Account: (
                UserBar(),
                ft.Row(controls=[NavigationBar(), DefaultArea()], expand=True),
                BottomBar(),
            ),
            PageState.Search: (
                UserBar(),
                ft.Row(controls=[NavigationBar(), SearchArea()], expand=True),
                BottomBar(),
            ),
            PageState.Settings: (
                UserBar(),
                ft.Row(controls=[NavigationBar(), SettingsArea()], expand=True),
                BottomBar(),
            )
        }
        self.view = ft.Column(controls=self.routes[PageState(self.page.route)], expand=True)

        self.page.add(self.view)
        self.page.on_route_change = lambda route: self.on_route_change()
        self.page.update()

        EVENT_HANDLER.subscribe(self, EventType.OnPageChanged)

    def go(self, page: PageState) -> None:
        self.page.go(page.value)

    def on_route_change(self) -> None:
        self.view.controls = self.routes[PageState(self.page.route)]
        self.view.update()
        self.page.update()

    def notify(self, data_manager: DataManager) -> None:
        self.go(data_manager.page)


def main(page: ft.Page) -> None:
    set_up_page_appearance(page)
    router = Router(page)
    page.dialog = Dialog()
    router.go(PageState(page.route))


ft.app(target=main, assets_dir=ASSETS_PATH)
