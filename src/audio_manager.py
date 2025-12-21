from pygame import mixer
from pathlib import Path

class audio_manager():
    def __init__(self, game):
        self.game = game
        mixer.init()
        self.sounds = self.load_files()

    def load_files(self):
        directory = Path("resources/audio")
        extensions = {".mp4", ".wav"}
        return {
            file.stem: mixer.Sound(str(file))
            for file in directory.iterdir()
            if file.is_file() and file.suffix.lower() in extensions
        }

    def play(self, name, volume=1):
        if not self.sounds[name]:
            return
        self.sounds[name].set_volume(self.game.config.get_float("volume") * volume)
        self.sounds[name].play()

    def stop(self, name):
        self.sounds[name].stop()


