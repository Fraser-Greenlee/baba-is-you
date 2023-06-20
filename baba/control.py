from typing import Optional

import pyxel


UP = '^'
DOWN = 'V'
LEFT = '<'
RIGHT = '>'
X = 'X'
Y = 'Y'

LAST_INPUT = None


def get_current_input() -> Optional[str]:
    if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT):
        return LEFT
    elif pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):
        return RIGHT
    elif pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_UP):
        return UP
    elif pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN):
        return DOWN
    elif pyxel.btn(pyxel.KEY_X) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_A):
        return X
    elif pyxel.btn(pyxel.KEY_C) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_B):
        return Y


def get_input() -> Optional[str]:
    global LAST_INPUT
    inp = get_current_input()
    if inp == LAST_INPUT:
        return
    inp = LAST_INPUT
    return inp
