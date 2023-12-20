import uuid
from Repository.repository import Repository
from Server.Application.Models.musicgenmodel import MusicGenModel
from Server.Domain.music_item import MusicItem
from Server.Application.Models.model_levels import ModelLevel
import torch

if torch.cuda.is_available():
    device = torch.device("cuda")
else:
    device = torch.device("cpu")
print("Using", device, "device")


DATA_PATH = "Repository/Data/"
CACHE_PATH = "Repository/Cache/"


class Application:
    def __init__(self):
        self.rep = Repository(data_path=DATA_PATH, cache_path=CACHE_PATH)
        self.model = MusicGenModel(ModelLevel.medium_model)

        self.APP_RUNNING = True

    def run(self):
        print("Server is upped")
        while self.APP_RUNNING:
            guess = input()
            if guess == "exit":
                self.APP_RUNNING = False
                continue
            self.add_music([guess])

    def add_music(self, params: list[str]):
        # "hard rock song with loud guitars and heavy drums"
        # "Eternal Harmony" is a captivating pop/rock anthem by Neon Dreams that combines vibrant instrumentals, powerful vocals, and an uplifting message of hope and unity.
        # an epic heavy rock song with blistering guitar, thunderous drums, fantasy-styled, fast temp with smooth end
        music_item = MusicItem(uuid.uuid4(), DATA_PATH, params, 3)
        self.model.generate(music_item).save()


if __name__ == "__main__":
    app = Application()
    app.run()
