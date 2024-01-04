import uvicorn
from server_settings import settings
from server_api import ServerAPI
from Server.ServerInterface.server_console_inteface import ServerConsoleInterface
from Server.Application.MusicRepository.music_repository import MusicRepository
from Server.Application.UserRepository.users_repository import UsersRepository
import threading


server_application = ServerAPI()
server_API = server_application.get_application()


def start_server():
    uvicorn.run(
        '__main__:server_API',
        host=settings.server_host,
        port=settings.server_port,
    )


thread = threading.Thread(target=start_server)
thread.start()

MUSIC_DATA_PATH = "../Application/MusicRepository/Data/"
MUSIC_CACHE_PATH = "../Application/MusicRepository/Cache/"
USERS_CACHE_PATH = "../Application/UserRepository/Cache/"
USERS_PASSWORDS_PATH = "../Application/UserRepository/Passwords/"
music_rep = MusicRepository(cache_path=MUSIC_CACHE_PATH, data_path=MUSIC_DATA_PATH)
users_rep = UsersRepository(cache_path=USERS_CACHE_PATH, passwords_path=USERS_PASSWORDS_PATH)

console = ServerConsoleInterface(music_rep, users_rep)
console.show_main_menu()
