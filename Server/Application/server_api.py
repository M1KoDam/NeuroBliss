from server_handlers import router
from fastapi import FastAPI


class ServerAPI:
    def __init__(self):
        self._application = FastAPI()
        self._application.include_router(router)

    def get_application(self) -> FastAPI:
        return self._application

