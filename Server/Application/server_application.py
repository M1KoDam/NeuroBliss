import threading
from Server.Application.MusicRepository.music_repository import MusicRepository
from Server.Application.UserRepository.users_repository import UsersRepository
from Server.Application.Models.musicgenmodel import MusicGenModel, ML_DICT
from Server.Domain.music_item import MusicItem, Status
from Server.Application.Models.model_levels import ModelLevel
from Server.Domain.user import User
import torch
import uuid

MUSIC_DATA_PATH = "../Application/MusicRepository/Data/"
MUSIC_CACHE_PATH = "../Application/MusicRepository/Cache/"
USERS_CACHE_PATH = "../Application/UserRepository/Cache/"
USERS_PASSWORDS_PATH = "../Application/UserRepository/Passwords/"


class ServerApplication:
    def __init__(self):
        self.default_device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        torch.set_default_device(self.default_device)

        self.music_rep = MusicRepository(cache_path=MUSIC_CACHE_PATH, data_path=MUSIC_DATA_PATH)
        self.users_rep = UsersRepository(cache_path=USERS_CACHE_PATH, passwords_path=USERS_PASSWORDS_PATH)
        self.model = MusicGenModel(ModelLevel.small_model)

        self.SERVER_AVAILABLE = False

        self._VERBOSE_INFO_OUTPUT = True

        self._tasks_limits = 3
        self._tasks: list[threading.Thread] = []
        self._tasks_queue: list[threading.Thread] = []

        self.queue: list[(User, MusicItem)] = []

    @property
    def VERBOSE_INFO_OUTPUT(self):
        return self._VERBOSE_INFO_OUTPUT

    def try_take_user_from_queue(self):
        if len(self.queue) == 0:
            return None

        if self.queue[0][1].status is Status.DONE:
            return self.queue.pop(0)
        return None

    def _generate_music(self, music_item: MusicItem):
        try:
            self.model.generate(music_item, verbose=self._VERBOSE_INFO_OUTPUT).save(verbose=self._VERBOSE_INFO_OUTPUT)
        except Exception as e:
            print("Generation failed with exception:\n{}".format(e))
        else:
            self.music_rep.add_music(music_item)

    def generate_music_by_phrase(self, user: User | None, params: list[str], length_in_seconds: int):
        # 90s rock song with loud guitars and heavy drums
        # "Eternal Harmony" is a captivating pop/rock anthem by Neon Dreams that combines vibrant instrumentals, powerful vocals, and an uplifting message of hope and unity.
        # an epic heavy rock song with blistering guitar, thunderous drums, fantasy-styled, fast temp with smooth end
        # Aggressive hard rock instrumental song with heavy drums, electric guitar
        music_item = MusicItem(str(uuid.uuid4()), MUSIC_DATA_PATH, params, length_in_seconds)
        if user is not None:
            self.queue.append((user, music_item))

        if self.default_device.__str__() == "cpu":
            thread = threading.Thread(target=self._generate_music,
                                      kwargs={'music_item': music_item})
            thread.start()
            self._tasks.append(thread)
        else:
            self._generate_music(music_item)

    def create_user(self):
        pass

    def change_device(self, new_device: str):
        """Set new device, for example cuda or cpu"""
        self.stop_server()

        if self.default_device == new_device:
            return
        print(f"Setting new device to {new_device}, please wait...")
        if new_device == "cuda":
            new_device = torch.device("cuda" if torch.cuda.is_available() else "cpu")  # cuda can be unavailable
        self.default_device = new_device
        torch.set_default_device(self.default_device)
        self.model.update_model()

    def change_model(self, new_model_level: ModelLevel):
        self.stop_server()
        self.model.change_model(new_model_level)

    def change_server_info_output(self):
        self._VERBOSE_INFO_OUTPUT = not self._VERBOSE_INFO_OUTPUT

    def stop_server(self):
        self.SERVER_AVAILABLE = False
        for task in self._tasks:
            task.join()
        self._tasks.clear()
