class configuration_manager():
    def __init__(self, game):
        self.game = game
        self.config = self.read_config("config")
        for bind in self.config["keybind"]:
            self.register_keybind(bind)

    def read_config(self, path):
        config = {}
        with open(path, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                key, value = line.split(None, 1)
                if key not in config:
                    config[key] = []
                config[key].append(value)
        return config

    def register_keybind(self, value):
        key, name = value.split(None, 1)
        self.game.io.register_keybind(name, key)

    def get_int(self, name):
        return int(self.config[name][0])

    def get_float(self, name):
        return float(self.config[name][0])

    def get_bool(self, name):
        return True if self.config[name] is "true" else False
