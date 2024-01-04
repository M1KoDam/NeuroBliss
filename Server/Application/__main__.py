import uvicorn
from server_settings import settings
from server_api import ServerAPI
import threading
# from __init__ import console


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


# console.show_main_menu()
