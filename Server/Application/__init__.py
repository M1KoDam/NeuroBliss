
def get_console():
    from Server.ServerInterface.server_console_inteface import ServerConsoleInterface

    return ServerConsoleInterface(get_music_repository(), get_users_repository())


def get_music_repository():
    MUSIC_DATA_PATH = "../Application/MusicRepository/Data/"
    MUSIC_CACHE_PATH = "../Application/MusicRepository/Cache/"

    from Server.Application.MusicRepository.music_repository import MusicRepository
    return MusicRepository(cache_path=MUSIC_CACHE_PATH, data_path=MUSIC_DATA_PATH)


def get_users_repository():
    USERS_CACHE_PATH = "../Application/UserRepository/Cache/"
    USERS_PASSWORDS_PATH = "../Application/UserRepository/Passwords/"

    from Server.Application.UserRepository.users_repository import UsersRepository
    return UsersRepository(cache_path=USERS_CACHE_PATH, passwords_path=USERS_PASSWORDS_PATH)
