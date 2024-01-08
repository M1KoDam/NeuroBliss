from ...core.event import EventDependent, EVENT_HANDLER, DATA_MANAGER, EventType, DataManager
from typing import Callable, Any
import flet as ft


class MyAudio(ft.Audio, EventDependent):
    def __init__(self, path: str, check_state: Callable[[Any], None]):
        EVENT_HANDLER.subscribe(self, EventType.OnPositionBySliderChanged)
        EVENT_HANDLER.subscribe(self, EventType.OnVolumeChanged)

        super().__init__(
            src=path,
            autoplay=True,
            volume=DATA_MANAGER.volume / 100,
            balance=0,
            on_position_changed=lambda e: DATA_MANAGER.raise_event(EventType.OnPositionChanged),
            on_state_changed=check_state
        )

    def notify(self, event: EventType, data_manager: DataManager) -> None:
        if event == EventType.OnVolumeChanged:
            self.volume = data_manager.volume
        elif event == EventType.OnPositionBySliderChanged:
            self.seek(self.get_duration() * data_manager.position_ratio)
