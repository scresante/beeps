# import adafruit_irremote
from adafruit_circuitplayground.express import cpx
from time import sleep

light = False
while True:
    print("temp: ", cpx.temperature)
    light = not light
    cpx.red_led = light
    sleep(5)
