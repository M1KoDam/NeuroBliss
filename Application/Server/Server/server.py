from Application.Server.Models.model import generate

if __name__ == "__main__":
    generate("pop_music",
             10,
             ["80s pop track with bassy drums and synth", "90s rock song with loud guitars and heavy drums"]
             )
