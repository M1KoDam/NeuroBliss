from transformers import AutoProcessor, MusicgenForConditionalGeneration
import scipy
from datetime import datetime
from Server.Domain.music_item import MusicItem
from Server.Application.Models.model_levels import ModelLevel, Medium


ONE_SECOND_PARAM = 51.2


class MusicGenModel:
    def __init__(self, model_level: ModelLevel):
        self._model_level = self.change_model(model_level)
        self._processor = AutoProcessor.from_pretrained(self._model_level)
        self.model = MusicgenForConditionalGeneration.from_pretrained(self._model_level)
        self.audio_values = None
        self.music_item = None

    def change_model(self, model_level: ModelLevel):
        if model_level is Medium:
            return "facebook/musicgen-medium"
        return "facebook/musicgen-small"

    def generate(self, music_item: MusicItem):
        self.music_item = music_item
        start_generation = datetime.now()
        print(f"Start generation music with next params:\n"
              f"Length: {music_item.length_in_seconds} sec\n"
              f"Model: {self._model_level}")
        inputs = self._processor(
            text=music_item.params,
            padding=True,
            return_tensors="pt",
        )

        self.audio_values = self.model.generate(**inputs, max_new_tokens=int(music_item.length_in_seconds * ONE_SECOND_PARAM))
        print(f"Generation end by {datetime.now() - start_generation}")
        return _ModelSave(self)


class _ModelSave:
    def __init__(self, model: MusicGenModel):
        self.model = model

    def save(self):
        print("saving...")
        sampling_rate = self.model.model.config.audio_encoder.sampling_rate
        scipy.io.wavfile.write(f"{self.model.music_item.path}{self.model.music_item.id}.wav", rate=sampling_rate,
                               data=self.model.audio_values[0, 0].numpy())
        return self.model
