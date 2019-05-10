import board
import digitalio

A = digitalio.DigitalInOut(board.BUTTON_A)
A.direction = digitalio.Direction.INPUT
A.pull = digitalio.Pull.DOWN

B = digitalio.DigitalInOut(board.BUTTON_B)
B.direction = digitalio.Direction.INPUT
B.pull = digitalio.Pull.DOWN

S = digitalio.DigitalInOut(board.SLIDE_SWITCH)
S.direction = digitalio.Direction.INPUT
S.pull = digitalio.Pull.UP

