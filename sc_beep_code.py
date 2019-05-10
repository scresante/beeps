import time
sleep = time.sleep
import array
import math
import audioio
import board
import digitalio
import buttons
from os import listdir

# enable the speaker
speaker_enable = digitalio.DigitalInOut(board.SPEAKER_ENABLE)
speaker_enable.direction = digitalio.Direction.OUTPUT
speaker_enable.value = True
audio = audioio.AudioOut(board.A0)

# modified wave helpers from adafruit_waveform to allow for volume control
def sine_wave(sample_frequency, pitch, vol=1.0):
    """Generate a single sine wav cycle at the given sampling frequency and pitch."""
    length = int(sample_frequency / pitch)
    b = array.array("H", [0] * length)
    for i in range(length):
        b[i] = int((math.sin(math.pi * 2 * i / length) * (2 ** 15) + 2 ** 15))
        b[i] = int(b[i]*vol)
    return b

def playtone(beepdata, samplerate=8000, waveform='sine', volume=0.5):
    ''' tone format is for beepdata is freq, dur, delay!!1'''
    freq, duration, delay = beepdata
    # print(beepdata)
    # print("freq %i dur %i delay %i" % (freq,duration,delay))
    if waveform == 'sine':
        wave_sample = audioio.RawSample(sine_wave(samplerate, freq, volume))
    if waveform == 'square':
        wave_sample = audioio.RawSample(square_wave(samplerate, freq))
    # repeat a wave sample for duration then wait for length
    audio.play(wave_sample, loop=True)
    time.sleep(duration/1000)
    audio.stop()
    time.sleep(delay/1000)

def playfile(beepfile):
    with open(beepfile, 'r') as f:
        read = eval(open(beepfile).read())
        for tone in read: 
            playtone(tone)
            if buttons.B.value:
                #TODO: use signals and debouncing
                sleep(0.2)
                return

def playintro(beepfile):
    ''' play the first MANY tones of a beepfile at SPEED  '''
    MANY = 8
    def qp(beepcode):
        freq, dur, delay = beepcode
        return (freq, dur*0.5, delay*0.5)
        # return (freq, dur, delay)
    with open(beepfile, 'r') as f:
        read = eval(open(beepfile).read())
        numtone = len(read)
        # slide read down to 20 or numtone, whichev is smaller
        if numtone <= MANY:
            read = read[:numtone]
        else:
            read = read[:MANY]
        print(len(read))
        for tone in read:
            playtone(qp(tone))

def gen_cycle_beepfiles():
    beepfile_list = []
    for beepfile in listdir('beeps'):
        if beepfile.find('0') != 0:
            beepfile_list.append('beeps/' + beepfile)
    # print(beepfile)
    while True:
        for f in beepfile_list:
            yield f

beepfile = gen_cycle_beepfiles()

# start on first file
cur_file = next(beepfile)
playintro(cur_file)

while True:
    #design a menu system
    if buttons.A.value: #cycle
        sleep(0.16)
        print('a')
        cur_file = next(beepfile)
        print('selected', cur_file)
        playintro(cur_file)

    if buttons.B.value: #play it
        print('b')
        sleep(0.2)
        print('playing', cur_file)
        playfile(cur_file)
        # because we don't know how to do interrupts in mainloops, 
        # implement interrupt back in playfile
