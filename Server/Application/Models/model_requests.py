from random import sample, choice


MOODS = {
    "happy": ["energetic", "uplifting", "groovy", "playful", "inspirational", "groovy"],
    "sad": ["melancholic", "emotional", "nostalgic", "dark", "soulful"],
    "calm": ["relaxed", "peaceful", "soulful", "thoughtful", "dreamy", "mysterious", "chill"],
    "aggressive": ["intense", "dark", "rebellious", "epic", "energetic"],
    "romantic": ["passionate", "mysterious"],
    "motivating": ["empowering", "inspirational", "epic", "uplifting"]
}

STYLES = {
    "happy": ["pop", "reggae", "disco", "funk", "club", "dubstep", "techno"],
    "sad": ["jazz", "blues", "sadcore", "dark ambient", "darkwave"],
    "calm": ["jazz", "ambient", "classical", "meditative"],
    "aggressive": ["rock", "metal", "punk", "hardcore", "heavy-metal", "dubstep"],
    "romantic": ["R&B", "soul", "jazz", "pop", "classical"],
    "motivating": ["hip-hop", "electronic", "pop", "rock", "dubstep"]
}

INSTRUMENTS = {
    "happy": ["guitar", "drums", "synth", "bass guitar"],
    "sad": ["violin", "piano", "saxophone", "acoustic guitar", "flute"],
    "calm": ["piano", "acoustic Guitar", "flute", "harp", "cello", "violin"],
    "aggressive": ["electric guitar", "bass guitar", "heavy drums", "synth"],
    "romantic": ["violin", "piano", "flute", "clarinet"],
    "motivating": ["electronic Drums", "electric Guitar", "synth", "trumpet", "drums"]
}


def get_model_request_by_mood(mood: str) -> str:
    moods = [mood, *sample(MOODS[mood], 2)]
    style = choice(STYLES[mood])
    instruments = sample(INSTRUMENTS[mood], 3)
    return f"{', '.join(moods)} {style} track with {', '.join(instruments[:-1])} and {instruments[-1]}"


if __name__ == "__main__":
    print(get_model_request_by_mood("romantic"))
