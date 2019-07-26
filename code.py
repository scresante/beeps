import sys
from adafruit_circuitplayground.express import cpx
import adafruit_irremote
import board
import pulseio
from time import sleep

if sys.platform != 'Atmel SAMD21':
    sys.path.append('/home/shawn/Code/circuitpython/libs')

# from digitalio import DigitalInOut, Direction, Pull
# Speaker as haptic feedback
# spkr_en = DigitalInOut(board.SPEAKER_ENABLE)
# spkr_en.direction = Direction.OUTPUT
# spkr_en.value = True
# spkr = DigitalInOut(board.SPEAKER)
# spkr.direction = Direction.OUTPUT
# led = DigitalInOut(board.D13)
# led.direction = Direction.OUTPUT

def recv_ir():
# Create a 'pulseio' input, to listen to infrared signals on the IR receiver
    pulsein = pulseio.PulseIn(board.IR_RX, maxlen=120, idle_state=True)
# Create a decoder that will take pulses and turn them into numbers
    decoder = adafruit_irremote.GenericDecode()

    while True:
        pulses = decoder.read_pulses(pulsein)
        try:
            # Attempt to convert received pulses into numbers
            received_code = decoder.decode_bits(pulses, debug=True)
        except adafruit_irremote.IRNECRepeatException:
            # We got an unusual short code, probably a 'repeat' signal
            print("NEC repeat!")
            continue
        except adafruit_irremote.IRDecodeException as e:
            # Something got distorted or maybe its not an NEC-type remote?
            print("Failed to decode: ", e.args)
            continue

        print("NEC Infrared code received: ", received_code)

def tx_ir():
# Create a 'pulseio' output, to send infrared signals on the IR transmitter @ 38KHz
    pwm = pulseio.PWMOut(board.IR_TX, frequency=38000, duty_cycle=2 ** 15)
    pulseout = pulseio.PulseOut(pwm)
# Create an encoder that will take numbers and turn them into NEC IR pulses
    encoder = adafruit_irremote.GenericTransmit(header=[9500, 4500], one=[550, 550], zero=[550, 1700], trail=0)

    codes = {"mute": [31, 31, 15, 240],
            "vol-": [31, 31, 47, 208],
            "vol+": [31, 31, 31, 224],}

    while True:
        break
        if buttons.A.value or buttons.B.value:
            encoder.transmit(pulseout, codes['mute'])
            print('button pressed, transmitting ' + str(codes['mute']))
        sleep(0.2)

# pulses = pulseio.PulseIn(board.IR_RX, maxlen=120, idle_state=True)
# decoder = adafruit_irremote.GenericDecode()

led = False
while True:
    if cpx.button_a:
        print('stopping')
        break
    if cpx.button_b:
        led = not led
        cpx.red_led = led
        while cpx.button_b:
            pass
    sleep(0.1)

