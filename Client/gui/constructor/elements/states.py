from enum import Enum


class VolumeIconState(Enum):
    Min = 0
    Med = 50
    Max = 100

    @staticmethod
    def from_volume(volume: int) -> 'VolumeIconState':
        if volume > 100 or volume < 0:
            raise ValueError
        elif volume == 100:
            return VolumeIconState.Max
        elif volume == 0:
            return VolumeIconState.Min
        else:
            return VolumeIconState.Med

    def get_value(self) -> int:
        return self.value


class VolumeStates:
    def __init__(self, cur_volume: int, prev_volume: int = None):
        self._cur_volume = cur_volume
        self._prev_volume = prev_volume

    def next(self) -> 'VolumeStates':
        if self._cur_volume == 0:
            if self._prev_volume is not None or self._prev_volume != 0:
                return VolumeStates(self._prev_volume, self._cur_volume)
            else:
                icon = VolumeIconState.Max
                return VolumeStates(icon.get_value(), self._cur_volume)
        icon = VolumeIconState.Min
        return VolumeStates(icon.get_value(), self._cur_volume)

    def get_volume(self) -> int:
        return self._cur_volume
