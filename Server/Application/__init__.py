def get_console():
    from Server.ServerInterface.server_console_inteface import ServerConsoleInterface

    return ServerConsoleInterface(get_music_repository(), get_users_repository(), get_server_application())


def get_server_application():
    from Server.Application.server_application import ServerApplication

    return ServerApplication(get_music_repository())


def get_music_repository():
    from Server.Application.MusicRepository.music_repository import MusicRepository

    MUSIC_DATA_PATH = "../Application/MusicRepository/Data/"

    return MusicRepository(music_data_path=MUSIC_DATA_PATH)


def get_users_repository():
    from Server.Application.UserRepository.users_repository import UsersRepository

    JSON_USERS_CACHE_PATH = "../Application/UserRepository/Data/"
    JSON_USERS_PASSWORDS_PATH = "../Application/UserRepository/Passwords/"

    return UsersRepository(user_data_path=JSON_USERS_CACHE_PATH, user_passwords_path=JSON_USERS_PASSWORDS_PATH)
