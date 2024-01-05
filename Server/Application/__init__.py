def get_console():
    from Server.ServerInterface.server_console_inteface import ServerConsoleInterface

    return ServerConsoleInterface(get_music_repository(), get_users_repository(), get_server_application())


def get_server_application():
    from Server.Application.server_application import ServerApplication

    return ServerApplication(get_music_repository())


def get_music_repository():
    from Server.Application.MusicRepository.music_repository import MusicRepository

    MUSIC_DATA_PATH = "../Application/MusicRepository/Data/"
    MUSIC_CACHE_PATH = "../Application/MusicRepository/Cache/"

    return MusicRepository(cache_path=MUSIC_CACHE_PATH, data_path=MUSIC_DATA_PATH)


def get_users_repository():
    from Server.Application.UserRepository.users_repository import UsersRepository

    USERS_CACHE_PATH = "../Application/UserRepository/Cache/"
    USERS_PASSWORDS_PATH = "../Application/UserRepository/Passwords/"

    return UsersRepository(cache_path=USERS_CACHE_PATH, passwords_path=USERS_PASSWORDS_PATH)
