# The MIT License (MIT)
#
# Copyright (c) 2017 Dan Halbert for Adafruit Industries
# Copyright (c) 2017 Kattni Rembor, Tony DiCola for Adafruit Industries
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# Some code is borrowed from here https://learn.adafruit.com/adafruit-circuit-playground-express/playground-sound-meter

import array
import math

import audiobusio
import board
import neopixel

# Factor de escala, en el rango -10 .. 10
CURVE = 2
SCALE_EXPONENT = math.pow(10, CURVE * -0.1)

NUM_PIXELS = 10
NUM_SAMPLES = 160

# Restringimos el valor entre el mínimo (floor) y el máximo (ceiling)
def constrain(value, floor, ceiling):
    return max(floor, min(value, ceiling))


# Escalamos el rango, exponencialmente, entre el mínimo y el m´maximo
def log_scale(input_value, input_min, input_max, output_min, output_max):
    normalized_input_value = (input_value - input_min) / (input_max - input_min)
    return output_min + math.pow(normalized_input_value, SCALE_EXPONENT) * (
        output_max - output_min
    )


# Calculo RMS normalizado
def normalized_rms(values):
    minbuf = int(mean(values))
    samples_sum = sum(float(sample - minbuf) * (sample - minbuf) for sample in values)

    return math.sqrt(samples_sum / len(values))


# Calculo de la media de los valores
def mean(values):
    return sum(values) / len(values)


# Códibo del vu-meter
def vumeter(magnitude):
    vu = [(0, 255, 0), (0, 255, 0), (255, 255, 0), (255, 255, 0), (255, 0, 0)]

    # Calculamos el nivel de sonido
    level = log_scale(
        constrain(magnitude, input_floor, input_ceiling),
        input_floor,
        input_ceiling,
        0,
        NUM_PIXELS // 2,
    )

    # Separamos la parte entera de los decimales
    bright, leds = math.modf(level)

    # La parte entera corresponde a los leds a iluminar
    leds = round(leds)

    pixels.fill((0, 0, 0))

    # Iluminamos los leds según la tabla de colores VU
    for l in range(leds):
        pixels[l] = vu[l]
        pixels[9 - l] = vu[l]

    # Si no hemos iluminado todos los leds, encendemos uno más según el color correspondiente con un factor de escala correspondiente a bright
    if leds < 4:
        dim = tuple(round(bright * x) for x in vu[leds + 1])
        pixels[leds] = dim
        pixels[9 - leds] = dim

    pixels.show()


# Programa principal

# Configuramos los neopixels y los apagamos
pixels = neopixel.NeoPixel(board.NEOPIXEL, NUM_PIXELS, brightness=0.1, auto_write=False)
pixels.fill(0)
pixels.show()

mic = audiobusio.PDMIn(
    board.MICROPHONE_CLOCK, board.MICROPHONE_DATA, sample_rate=16000, bit_depth=16
)

# Calibramos el vu-meter. Se asume que este será el valor mínimo, silencio.
samples = array.array("H", [0] * NUM_SAMPLES)
mic.record(samples, len(samples))
input_floor = normalized_rms(samples) + 10

# Ajustamos la sensibilidad
sensitivity = 500
input_ceiling = input_floor + sensitivity

while True:
    mic.record(samples, len(samples))
    magnitude = normalized_rms(samples)
    vumeter(magnitude)
