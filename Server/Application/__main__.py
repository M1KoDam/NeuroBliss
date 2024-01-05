import uvicorn
from server_settings import settings
from server_api import ServerAPI
import threading
from __init__ import get_console


def start_server():
    uvicorn.run(
        '__main__:server_API',
        host=settings.server_host,
        port=settings.server_port,
    )


server_application = ServerAPI()
server_API = server_application.get_application()
threading.Thread(target=start_server).start()

console = get_console()
console.show_main_menu()
