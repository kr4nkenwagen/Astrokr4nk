from pygame import mixer
from pathlib import Path

class audio_manager():
    def __init__(self, game):
        self.game = game
        mixer.init()
        mixer.set_num_channels(512)
        self.sounds = self.load_files()
        self.active_channels = {}

    def load_files(self):
        directory = Path("resources/audio")
        extensions = {".mp4", ".wav"}
        return {
            file.stem: mixer.Sound(str(file))
            for file in directory.iterdir()
            if file.is_file() and file.suffix.lower() in extensions
        }

    def play(self, name, volume=1, loop=False):
        if loop and self.is_playing(name):
            return
        sound = self.sounds.get(name)
        if not sound:
            return
        sound.set_volume(clamp_audio((self.game.config.get_float("volume") * volume)))
        channel = mixer.find_channel()
        if channel:
            loops = -1 if loop else 0
            channel.play(sound, loops=loops)
            self.active_channels[name] = channel

    def stop(self, name):
        channel = self.active_channels.get(name)
        if channel:
            channel.stop()
            del self.active_channels[name]

    def is_playing(self, name):
        channel = self.active_channels.get(name)
        if not channel:
            return False
        if channel.get_busy():
            return True
        del self.active_channels[name]
        return False

    def set_channel_audio(self, name, volume):
        channel = self.active_channels.get(name)
        if channel:
            channel.set_volume(clamp_audio(self.game.config.get_float("volume") * volume))

def clamp_audio(volume):
    return max(0.0, min(1.0, volume))
