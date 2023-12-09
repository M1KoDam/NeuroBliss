from transformers import AutoProcessor, MusicgenForConditionalGeneration
import scipy
from datetime import datetime


DATA_PATH = "../Repository/Data/"
ONE_SECOND_PARAM = 51.2


def generate(music_name: str,
             length_in_seconds: int,
             params: list,
             model_level=1):
    start_generation = datetime.now()
    model_leval = "facebook/musicgen-small" if model_level else "facebook/musicgen-medium"
    print(f"Start generation music with next params:\n"
          f"Name: {music_name}\n"
          f"Length: {length_in_seconds} sec\n"
          f"Model: {'Small' if model_level else 'Medium'}")

    processor = AutoProcessor.from_pretrained(model_leval)
    model = MusicgenForConditionalGeneration.from_pretrained(model_leval)

    inputs = processor(
        text=params,
        padding=True,
        return_tensors="pt",
    )

    audio_values = model.generate(**inputs, max_new_tokens=int(length_in_seconds*ONE_SECOND_PARAM))

    sampling_rate = model.config.audio_encoder.sampling_rate
    scipy.io.wavfile.write(f"{DATA_PATH}{music_name}.wav", rate=sampling_rate, data=audio_values[0, 0].numpy())

    print(f"Generation end by {datetime.now()-start_generation}")
