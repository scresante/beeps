# circpy 5.3.1 
from array import array
from adafruit_circuitplayground import cp
from time import sleep
import board
import pulseio
import adafruit_irremote

pwm = pulseio.PWMOut(board.REMOTEOUT, frequency=38000,
                     duty_cycle=2 ** 15, variable_frequency=True)
pulseout = pulseio.PulseOut(pwm)

def samsung_power():
    code = {'freq':38338, 'delay':0.25, 'repeat':2, 'repeat_delay':0.046,
            'table':[[4460,4500],[573,1680],[573,567]],
            'index':[0,1,1,1,2,2,2,2,2,1,1,1,2,2,2,2,2,2,1,2,2,2,2,2,2,1,2,1,1,1,1,1,1,1]}
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
        pulseout.send(array('H', pulses))
        sleep(delay)

codes = {
        "mute": [31, 31, 15, 240], "vol+": [31, 31, 31, 224],
        "vol-": [31, 31, 47, 208], '0': [31, 31, 119, 136],
        '1': [31, 31, 223, 32], '2': [31, 31, 95, 160],
        '3': [31, 31, 159, 96], '4': [31, 31, 239, 16],
        '5': [31, 31, 111, 144], '6': [31, 31, 175, 80],
        '7': [31, 31, 207, 48], '8': [31, 31, 79, 176],
        '9': [31, 31, 143, 112], 'dash': [31, 31, 59, 196],
        'down': [31, 31, 121, 134], 'exit': [31, 31, 75, 180],
        'info': [31, 31, 7, 248], 'left': [31, 31, 89, 166],
        'menu': [31, 31, 167, 88], 'power': [31, 31, 191, 64],
        'prevchan': [31, 31, 55, 200], 'psize': [31, 31, 131, 124],
        'return': [31, 31, 229, 26], 'right': [31, 31, 185, 70],
        'select': [31, 31, 233, 22], 'source': [31, 31, 127, 128],
        'tools': [31, 31, 45, 210], 'up': [31, 31, 249, 6],
        }


# Create an encoder that will take numbers and turn them into NEC IR pulses
encoder = adafruit_irremote.GenericTransmit(header=[4460, 4500], one=[573, 573],
                                            zero=[573, 1680], trail=0)

print('switch is: ' + str(cp.switch))
sw = {False: 'send', True: 'load'}

while True:
    if cp.button_a:
        print("Temp: ", cp.temperature)
        print("sending encoded mute")
        encoder.transmit(pulseout, codes['mute'])
    if cp.button_b:
        print("sending power")
        samsung_power()
    if cp.touch_A1:
        pass
    if cp.touch_A2:
        print("sending encoded power")
        encoder.transmit(pulseout, codes['power'])
        pass
    if cp.touch_A3:
        pass
    if cp.touch_A4:
        print("sending encoded vol+")
        encoder.transmit(pulseout, codes['vol+'])
        pass
    if cp.touch_A5:
        print("sending encoded source")
        encoder.transmit(pulseout, codes['source'])
        pass
    if cp.touch_A6:
        print("sending encoded power")
        encoder.transmit(pulseout, codes['power'])
        pass
    if cp.touch_A7:
        print("sending encoded vol-")
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

