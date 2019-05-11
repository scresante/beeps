import time
import board
from digitalio import DigitalInOut, Direction, Pull
import audioio
from os import listdir
from neopixel_demo import simpleCircle

# The pad our button is connected to:
button = DigitalInOut(board.A4)
button.direction = Direction.INPUT
button.pull = Pull.UP

wavdir = 'menuwavs/'
wavtestlist = [ wavdir+_ for _ in listdir(wavdir) ]

# Audio Play File
def play_file(playname):
    print("Playing File " + playname)
    wave_file = open(playname, "rb")
    with audioio.WaveFile(wave_file) as wave:
        with audioio.AudioOut(board.A0) as audio:
            audio.play(wave)
            while audio.playing:
                simpleCircle(.02)
    print("finished")

for filename in wavtestlist[0:2]:
# while True:
    # if not button.value:
    play_file(filename)