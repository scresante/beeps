from adafruit_circuitplayground import cp
from time import sleep
import board
import pulseio
import adafruit_irremote
import supervisor
supervisor.disable_autoreload()

def recv_ir():
# use this function to grab codes from the remote
    print('receiving')
# Create a 'pulseio' input, to listen to infrared signals on the IR receiver
    pulsein = pulseio.PulseIn(board.IR_RX, maxlen=120, idle_state=True)
# Create a decoder that will take pulses and turn them into numbers
    decoder = adafruit_irremote.GenericDecode()

    while True:
        pulses = decoder.read_pulses(pulsein)
        try:
            if not cp.switch:
                pulsein.deinit()
                return None
            # Attempt to convert received pulses into numbers
            received_code = decoder.decode_bits(pulses)
        except adafruit_irremote.IRNECRepeatException:
            # We got an unusual short code, probably a 'repeat' signal
            print("NEC repeat!")
            continue
        except adafruit_irremote.IRDecodeException as e:
            # Something got distorted or maybe its not an NEC-type remote?
            print("Failed to decode: ", e.args)
            continue

        print("NEC Infrared code received: ", received_code)
        print("enter key: ",end='')
        name = input()
        pulsein.deinit()
        return((name,received_code))


def tx_ir(code):
    ''' dont use this, headers and timing bits are wrong for samsung '''
# Create a 'pulseio' output, to send infrared signals on the IR transmitter @ 38KHz
    pwm = pulseio.PWMOut(board.IR_TX, frequency=38000, duty_cycle=2 ** 15)
    pulseout = pulseio.PulseOut(pwm)
# Create an encoder that will take numbers and turn them into NEC IR pulses
    encoder = adafruit_irremote.GenericTransmit(header=[4460, 4500], one=[573, 573],
                                                    zero=[573, 1680], trail=0)
    codes = {"mute": [31, 31, 15, 240],
            "vol-": [31, 31, 47, 208],
            "vol+": [31, 31, 31, 224],
            'power': [31, 31, 191, 64]}

    encoder.transmit(pulseout, codes[code])
    print(code + ' button pressed, transmitting ' + str(codes[code]))
    pulseout.deinit()
    pwm.deinit()

def recv_main():
    keydict = {}
    while True:
        if cp.switch:
            # capture mode
            cp.pixels.fill((0,30,10))
            code = recv_ir()
            if code:
                # store the tuple as the keypress description
                keydict[code[0]] = code[1]
            else:
                # code is None? print keydict and die
                print(keydict)
                break
            # print(code)
        else:
            # transmit mode
            cp.pixels.fill((30,0,0))
            if cp.button_a:
                tx_ir('power')
            if cp.button_b:
                tx_ir('mute')
        sleep(0.05)

recv_main()
