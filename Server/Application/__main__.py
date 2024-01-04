import uvicorn
from server_settings import settings
from server_api import ServerAPI
from Server.ServerInterface.server_console_inteface import ServerConsoleInterface

server_application = ServerAPI()
server_API = server_application.get_application()

console = ServerConsoleInterface()
console.show_main_menu()
app = console.server_app

uvicorn.run(
    '__main__:server_API',
    host=settings.server_host,
    port=settings.server_port,
)
