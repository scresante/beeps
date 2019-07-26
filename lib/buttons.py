import board
from digitalio import DigitalInOut, Direction, Pull

A = DigitalInOut(board.BUTTON_A)
A.direction = Direction.INPUT
A.pull = Pull.DOWN

B = DigitalInOut(board.BUTTON_B)
B.direction = Direction.INPUT
B.pull = Pull.DOWN

S = DigitalInOut(board.SLIDE_SWITCH)
S.direction = Direction.INPUT
S.pull = Pull.UP

