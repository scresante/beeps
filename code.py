import sys
sys.path.append('/home/shawn/Code/circuitpython/libs')
# from adafruit_circuitplayground.express import cpx
from adafruit_circuitplayground import cp
import board
import pulseio
import adafruit_irremote
from time import sleep
# def recv_ir():
    # print('receiving')
# # Create a 'pulseio' input, to listen to infrared signals on the IR receiver
    # pulsein = pulseio.PulseIn(board.IR_RX, maxlen=120, idle_state=True)
# # Create a decoder that will take pulses and turn them into numbers
    # decoder = adafruit_irremote.GenericDecode()

    # while True:
        # if cpx.button_a or cpx.button_b:
            # print('cancel')
            # pulsein.deinit()
            # return None
        # pulses = decoder.read_pulses(pulsein)
        # try:
            # # Attempt to convert received pulses into numbers
            # received_code = decoder.decode_bits(pulses, debug=False)
        # except adafruit_irremote.IRNECRepeatException:
            # # We got an unusual short code, probably a 'repeat' signal
            # print("NEC repeat!")
            # continue
        # except adafruit_irremote.IRDecodeException as e:
            # # Something got distorted or maybe its not an NEC-type remote?
            # print("Failed to decode: ", e.args)
            # continue

        # print("NEC Infrared code received: ", received_code)
        # pulsein.deinit()
        # return(received_code)

# def tx_ir(code):
# # Create a 'pulseio' output, to send infrared signals on the IR transmitter @ 38KHz
    # pwm = pulseio.PWMOut(board.IR_TX, frequency=38000, duty_cycle=2 ** 15)
    # pulseout = pulseio.PulseOut(pwm)
# # Create an encoder that will take numbers and turn them into NEC IR pulses
    # encoder = adafruit_irremote.GenericTransmit(header=[9500, 4500], one=[550, 550], zero=[550, 1700], trail=0)

    # codes = {"mute": [31, 31, 15, 240],
            # "vol-": [31, 31, 47, 208],
            # "vol+": [31, 31, 31, 224],
            # 'power': [31, 31, 191, 64]}

    # encoder.transmit(pulseout, codes[code])
    # print(code + ' button pressed, transmitting ' + str(codes[code]))
    # pulseout.deinit()
    # pwm.deinit()

pwm = pulseio.PWMOut(board.IR_TX, frequency=38000, duty_cycle=2 ** 15)
pulseout = pulseio.PulseOut(pwm)
# Create an encoder that will take numbers and turn them into NEC IR pulses
encoder = adafruit_irremote.GenericTransmit(header=[9500, 4500], one=[550, 550],
                                                    zero=[550, 1700], trail=0)
codes = {"mute": [31, 31, 15, 240],
        "vol-": [31, 31, 47, 208],
        "vol+": [31, 31, 31, 224],
        'power': [31, 31, 191, 64]}

print('switch is: ' + str(cp.switch))
sw = {False: 'send', True: 'load'}

while True:
    if cp.button_a:
        print("Temp: ", cp.temperature)
        print("sending mute")
        encoder.transmit(pulseout, codes['mute'])
    if cp.button_b:
        print("sending power")
        encoder.transmit(pulseout, codes['power'])
    if cp.touch_A1:
        pass
    if cp.touch_A2:
        pass
    if cp.touch_A3:
        pass
    if cp.touch_A4:
        pass
    if cp.touch_A5:
        pass
    if cp.touch_A6:
        pass
    if cp.touch_A7:
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

# while True:
    # if cpx.switch:
        # # capture mode
        # cpx.pixels.fill(0)
        # cpx.pixels[0] = [0,8,0]
        # code = recv_ir()
        # print(code)
    # else:
        # # transmit mode
        # cpx.pixels.fill(0)
        # cpx.pixels[9] = [8,0,0]
        # if cpx.button_a:
            # tx_ir('power')
        # if cpx.button_b:
            # tx_ir('mute')
    # sleep(0.05)
