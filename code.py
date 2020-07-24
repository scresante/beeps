import sys
import array
from adafruit_circuitplayground import cp
import board
import pulseio
import adafruit_irremote
import time
import recv

pwm = pulseio.PWMOut(board.REMOTEOUT, frequency=38000,
                     duty_cycle=2 ** 15, variable_frequency=True)
pulseout = pulseio.PulseOut(pwm)

def samsung_power():
    code = {'freq':38338,'delay':0.25,'repeat':2,'repeat_delay':0.046,'table':[[4460,4500],[573,1680],[573,567]],'index':[0,1,1,1,2,2,2,2,2,1,1,1,2,2,2,2,2,2,1,2,2,2,2,2,2,1,2,1,1,1,1,1,1,1]}
    repeat = code['repeat']
    delay = code['repeat_delay']
    table = code['table']
    pulses = []  # store the pulses here
    # Read through each indexed element
    for i in code['index']:
        pulses += table[i]  # and add to the list of pulses
    pulses.pop()  # remove one final 'low' pulse

    pwm.frequency = code['freq']
    for i in range(repeat):
        pulseout.send(array.array('H', pulses))
        print(array.array('H', pulses))
        time.sleep(delay)

codes = {"mute": [31, 31, 15, 240],
        "vol-": [31, 31, 47, 208],
        "vol+": [31, 31, 31, 224],
        'power': [31, 31, 191, 64]}
# Create an encoder that will take numbers and turn them into NEC IR pulses
encoder = adafruit_irremote.GenericTransmit(header=[4460, 4500], one=[573, 573],
                                                    zero=[573, 1680], trail=0)

print('switch is: ' + str(cp.switch))
sw = {False: 'send', True: 'load'}

while True:
    if cp.button_a:
        print("Temp: ", cp.temperature)
        print("sending encoder mute")
        encoder.transmit(pulseout, codes['mute'])
    if cp.button_b:
        print("sending power")
        samsung_power()
    if cp.touch_A1:
        pass
    if cp.touch_A2:
        print("sending encoder power")
        encoder.transmit(pulseout, codes['power'])
        pass
    if cp.touch_A3:
        pass
    if cp.touch_A4:
        print("sending encoder vol+")
        encoder.transmit(pulseout, codes['vol+'])
        pass
    if cp.touch_A5:
        pass
    if cp.touch_A6:
        pass
    if cp.touch_A7:
        print("sending encoder vol-")
        encoder.transmit(pulseout, codes['vol-'])
        pass
    cp.red_led = cp.button_b
    if cp.switch:
        while cp.switch:
            cp.pixels.fill((255,0,0))
            cp.play_tone(100,0.2)
            cp.pixels.fill((0,255,0))
            cp.play_tone(100,0.2)
            cp.pixels.fill((0,0,255))
            cp.play_tone(100,0.2)
    else:
        cp.pixels.fill(0)

