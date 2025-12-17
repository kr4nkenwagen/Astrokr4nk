import pygame
from enum import Enum
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

    def key_translation(self, str):
        str = str.lower()
        NUMBER_ALIASES = {
            "0": "zero", "1": "one", "2": "two", "3": "three", "4": "four",
            "5": "five", "6": "six", "7": "seven", "8": "eight", "9": "nine",
        }
        if str in NUMBER_ALIASES:
            str = NUMBER_ALIASES[str]
        if str == "return":
            str = "return_"
        return internal_key[str].value

    def register_keybind(self, name, key):
        key = self.key_translation(key)
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

class internal_key(Enum):
    backspace = pygame.K_BACKSPACE
    tab = pygame.K_TAB
    clear = pygame.K_CLEAR
    return_ = pygame.K_RETURN
    pause = pygame.K_PAUSE
    escape = pygame.K_ESCAPE
    space = pygame.K_SPACE
    delete = pygame.K_DELETE

    # Numbers
    zero = pygame.K_0
    one = pygame.K_1
    two = pygame.K_2
    three = pygame.K_3
    four = pygame.K_4
    five = pygame.K_5
    six = pygame.K_6
    seven = pygame.K_7
    eight = pygame.K_8
    nine = pygame.K_9

    # Letters
    a = pygame.K_a
    b = pygame.K_b
    c = pygame.K_c
    d = pygame.K_d
    e = pygame.K_e
    f = pygame.K_f
    g = pygame.K_g
    h = pygame.K_h
    i = pygame.K_i
    j = pygame.K_j
    k = pygame.K_k
    l = pygame.K_l
    m = pygame.K_m
    n = pygame.K_n
    o = pygame.K_o
    p = pygame.K_p
    q = pygame.K_q
    r = pygame.K_r
    s = pygame.K_s
    t = pygame.K_t
    u = pygame.K_u
    v = pygame.K_v
    w = pygame.K_w
    x = pygame.K_x
    y = pygame.K_y
    z = pygame.K_z

    # Punctuation / symbols
    comma = pygame.K_COMMA
    period = pygame.K_PERIOD
    slash = pygame.K_SLASH
    minus = pygame.K_MINUS
    equals = pygame.K_EQUALS
    semicolon = pygame.K_SEMICOLON
    quote = pygame.K_QUOTE
    left_bracket = pygame.K_LEFTBRACKET
    right_bracket = pygame.K_RIGHTBRACKET
    backslash = pygame.K_BACKSLASH
    backquote = pygame.K_BACKQUOTE

    # Arrows
    up = pygame.K_UP
    down = pygame.K_DOWN
    left = pygame.K_LEFT
    right = pygame.K_RIGHT

    # Modifiers
    left_shift = pygame.K_LSHIFT
    right_shift = pygame.K_RSHIFT
    left_ctrl = pygame.K_LCTRL
    right_ctrl = pygame.K_RCTRL
    left_alt = pygame.K_LALT
    right_alt = pygame.K_RALT

    # Function keys
    f1 = pygame.K_F1
    f2 = pygame.K_F2
    f3 = pygame.K_F3
    f4 = pygame.K_F4
    f5 = pygame.K_F5
    f6 = pygame.K_F6
    f7 = pygame.K_F7
    f8 = pygame.K_F8
    f9 = pygame.K_F9
    f10 = pygame.K_F10
    f11 = pygame.K_F11
    f12 = pygame.K_F12
