from adafruit_circuitplayground.express import cpx
from time import sleep
import time
import adafruit_irremote
import pulseio
import board
import ir

# Create a 'pulseio' input, to listen to infrared signals on the IR receiver
pulsein = pulseio.PulseIn(board.IR_RX, maxlen=120, idle_state=True)
# Create a necoder that will take pulses and turn them into numbers
decoder = adafruit_irremote.GenericDecode()

# NeoPixel Animation
def simpleCircle(wait):
    pixels = cpx.pixels 
    PURPLE = (255, 0, 255)
    BLACK = (0, 0, 0)
    CYAN = (0, 255, 255)
    ORANGE = (255, 255, 0)
    for i in range(len(pixels)):
        pixels[i] = PURPLE
        time.sleep(wait)
    for i in range(len(pixels)):
        pixels[i] = CYAN
        time.sleep(wait)
    for i in range(len(pixels)):
        pixels[i] = ORANGE
        time.sleep(wait)
    for i in range(len(pixels)):
        pixels[i] = BLACK
        time.sleep(wait)

light = True
print("ON..............>>")

while False:
    if cpx.button_a:
        cpx.play_file('menuwavs/test.wav')
        cpx.red_led = light
        print("temp: ", cpx.temperature)
        simpleCircle(0.02)
        sleep(1)
    light = not light
    irbutton = ir.get_ir(decoder, pulsein)
    print(irbutton)
    wav = 'menuwavs/' + irbutton + '.wav'
    print('playing %s' % wav)
    if irbutton.isdigit():
        print('its a button')
        simpleCircle(0.02)
        cpx.play_file(wav)
    light = True
    cpx.red_led = light
    sleep(1)
    light = False
    cpx.red_led = light

# non blocking looop demo
import nonblocking_timer

# G = (0, 100, 0)
# O = (100, 100, 0)
# R = (100, 0, 0)
# pixels = cpx.pixels
# for c in [G, O, R]:
    # for i in range(10):
        # pixels[i] = c
        # while time.monotonic() - now < 0.5:
            # pass
# pixels.fill(0)

class BlinkDemo(nonblocking_timer):
    def __init__(self):
        super(BlinkDemo, self).__init__(0.1)
        self.led = digitalio.DigitalInOut(board.D13)
        self.led.direction = digitalio.Direction.OUTPUT
        self.value = True

    def stop(self):
        self.led.value = False

    def next(self):
        if super(BlinkDemo, self).next():
            self.led.value = not (self.led.value)

blinkdemo.BlinkDemo()

while True:
    blinkDemo.next()
    # This is the only place you should use time.sleep: to set the overall
    # "sampling rate" of your program.
    time.sleep(0.001)
