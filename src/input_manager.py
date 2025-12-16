from pygame import key
class input_manager:
    registered_keybinds = []

    def __init__(self, game):
        self.game = game
        pass

    def update(self):
        keys = key.get_pressed()
        for reg_key in self.registered_keybinds:
            state = keys[reg_key["key"]]
            reg_key["released"] = not state and reg_key["down"]
            reg_key["pressed"] = not reg_key["down"] and state
            reg_key["down"] = state



    def register_keybind(self, name, key):
        self.registered_keybinds.append(
            {
                "key": key,
                "name": name,
                "pressed": False,
                "down": False,
                "released": False

            }
        )

    def is_pressed(self, name):
        for reg_key in self.registered_keybinds:
            if reg_key["name"] == name:
                return reg_key["pressed"]
        return False

    def is_down(self, name):
        for reg_key in self.registered_keybinds:
            if reg_key["name"] == name:
                return reg_key["down"]
        return False

    def is_released(self, name):
        for reg_key in self.registered_keybinds:
            if reg_key["name"] == name:
                return reg_key["released"]
        return False
