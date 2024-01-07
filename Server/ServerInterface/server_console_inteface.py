from Server.Application.Models.model_levels import ModelLevel
from Server.Application.Models.musicgenmodel import ML_DICT
from Server.ServerInterface.server_menus import ServerMenu


def confirm_action(action):
    console_confirmation = input(f"\nAre you sure you want to {action}? (y/n): ")
    if console_confirmation == 'y':
        return True
    return False


def generate_menu(text_func, options: list, options_args: list[tuple]):
    assert len(options) == len(options_args)
    print(text_func())
    console_input = input(">>> Your choice: ")
    while console_input not in ('0',):
        for option_index in range(len(options)):
            if console_input in (str(option_index + 1),):
                options[option_index](*options_args[option_index])
                break
        else:
            print("Invalid input")

        print(text_func())
        console_input = input(">>> Your choice: ")


class ServerConsoleInterface:
    __instance = None

    def __init__(self, music_rep, users_rep, server_app):
        if self.__initialized:
            return
        self.__initialized = True

        print("INIT ServerConsoleInterface")
        self.music_rep = music_rep
        self.users_rep = users_rep
        self.server_app = server_app
        self._CONSOLE_RUNNING = True

    def up_server(self):
        print(f"""Server is upped with next parameters:
Model: {ML_DICT[self.server_app.model.model_level]}
Device: {self.server_app.default_device.__str__()}
Verbose: {self.server_app.VERBOSE_INFO_OUTPUT}""")

        self.server_app.SERVER_AVAILABLE = True

    def show_main_menu(self):
        self.up_server()
        generate_menu(ServerMenu.get_main_menu_banner,
                      [
                          self.generate_music_by_console,
                          self.show_users_info,
                          self.show_musics_info,
                          self.show_options],
                      [(), (), (), ()]
                      )

    def show_users_info(self):
        generate_menu(ServerMenu.get_user_info_menu_banner,
                      [
                          self.get_user_by_enter_id,
                          self.delete_user_by_enter_id,
                          self.clear_users],
                      [(), (), ()]
                      )

    def show_musics_info(self):
        generate_menu(ServerMenu.get_music_info_menu_banner,
                      [
                          self.get_music_by_enter_id,
                          self.delete_music_by_enter_id,
                          self.clear_music],
                      [(), (), ()]
                      )

    def generate_music_by_console(self):
        input_phrase = input(">>> Choose one of six moods (happy, sad, calm, aggressive, romantic, motivating)"
                             " or enter your phrase: ")
        try:
            input_seconds = int(input(">>> Enter the duration in seconds (5-30): "))
            if not 5 <= input_seconds <= 30:
                raise ValueError
        except ValueError:
            print("Invalid seconds input")
            return
        self.server_app.generate_music_by_phrase(input_phrase, input_seconds)

    def get_user_by_enter_id(self):
        self.users_rep.get_user_by_id(input(">>> Enter user id: "))

    def delete_user_by_enter_id(self):
        self.users_rep.delete_user_by_id(input(">>> Enter user id: "))

    def clear_users(self):
        if confirm_action("delete all users"):
            self.users_rep.clear()
            print("Users has been deleted successfully")

    def get_music_by_enter_id(self):
        self.music_rep.get_music_by_id(input(">>> Enter music id: "))

    def delete_music_by_enter_id(self):
        self.music_rep.delete_music_by_id(input(">>> Enter music id: "))

    def clear_music(self):
        if confirm_action("delete all music"):
            self.music_rep.clear()
            print("Music has been deleted successfully")

    def get_options_menu(self):
        return f"""\nOptions
----------
Model:
1. [{"X" if self.server_app.model.model_level is ModelLevel.small_model else " "}] facebook/musicgen-small
2. [{"X" if self.server_app.model.model_level is ModelLevel.medium_model else " "}] facebook/musicgen-medium
Device:
3. [{"X" if self.server_app.default_device.__str__() == "cpu" else " "}] CPU (multithreading available)
4. [{"X" if self.server_app.default_device.__str__() == "cuda" else " "}] CUDA
Info output:
5. ({"X" if self.server_app.VERBOSE_INFO_OUTPUT else " "}) Verbose
----------
0. Back"""

    def show_options(self):
        generate_menu(self.get_options_menu,
                      [
                          self.server_app.change_model,
                          self.server_app.change_model,
                          self.server_app.change_device,
                          self.server_app.change_device,
                          self.server_app.change_server_info_output
                      ],
                      [
                          (ModelLevel.small_model,), (ModelLevel.medium_model,),
                          ("cpu",), ("cuda",), ()
                      ]
                      )

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__initialized = False
        return cls.__instance
