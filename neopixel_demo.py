import neopixel
import board
pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=1)
# NeoPixel Animation
def simpleCircle(wait):
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

