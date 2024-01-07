from transformers import AutoProcessor, MusicgenForConditionalGeneration
import scipy
from datetime import datetime
from Server.Domain.music_item import MusicItem
from Server.Application.Models.model_levels import ModelLevel

ONE_SECOND_PARAM = 51.2
ML_DICT = {ModelLevel.small_model: "facebook/musicgen-small",
           ModelLevel.medium_model: "facebook/musicgen-medium"}


class MusicGenModel:
    def __init__(self, model_level: ModelLevel):
        self.model_level = model_level
        self.change_model(model_level)
        self._processor = AutoProcessor.from_pretrained(ML_DICT[self.model_level])
        self.model = MusicgenForConditionalGeneration.from_pretrained(ML_DICT[self.model_level])
        self.audio_values = None
        self.music_item = None

    def update_model(self):
        self._processor = AutoProcessor.from_pretrained(ML_DICT[self.model_level])
        self.model = MusicgenForConditionalGeneration.from_pretrained(ML_DICT[self.model_level])

    def change_model(self, new_model_level: ModelLevel):
        print(f"Set up {ML_DICT[new_model_level]} model, please wait...")
        if new_model_level == self.model_level:
            return
        self.model_level = new_model_level
        self.model = MusicgenForConditionalGeneration.from_pretrained(ML_DICT[new_model_level])

    def generate(self, music_item: MusicItem, verbose=False):
        self.music_item = music_item
        start_generation = datetime.now()
        if verbose:
            print(f"\nStart generation music with next params:\n"
                  f"Phrase: {music_item.phrase}\n"
                  f"Length: {music_item.length_in_seconds} sec\n"
                  f"Model: {ML_DICT[self.model_level]}")
        inputs = self._processor(
            text=[music_item.phrase],
            padding=True,
            return_tensors="pt",
        )

        self.audio_values = self.model.generate(**inputs,
                                                max_new_tokens=int(music_item.length_in_seconds * ONE_SECOND_PARAM))
        if verbose:
            print(f"Generation end by {datetime.now() - start_generation}")
        return _ModelSave(self)


class _ModelSave:
    def __init__(self, model: MusicGenModel):
        self.model = model

    def save(self, verbose=False):
        if verbose:
            print("\nStart saving...")
        sampling_rate = self.model.model.config.audio_encoder.sampling_rate
        scipy.io.wavfile.write(f"{self.model.music_item.path}{self.model.music_item.id}.wav", rate=sampling_rate,
                               data=self.model.audio_values[0, 0].cpu().numpy())
        if verbose:
            print(f"Saved successfully with id = {self.model.music_item.id}")
        self.model.music_item.is_ready = True
        return self.model
