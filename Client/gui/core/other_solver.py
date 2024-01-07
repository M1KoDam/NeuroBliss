from .data import User, AppData, PlayState, Singleton
from .event import ConnectionType, EventSolver, EVENT_HANDLER, DataManager, EventType
from os import getcwd
from pathlib import Path


class PlaySolver(EventSolver, metaclass=Singleton):
    def notify(self, data_manager: DataManager):
        if data_manager.connection is ConnectionType.Online:
            if data_manager.play == PlayState.PlayFromGeneration:
                ...


