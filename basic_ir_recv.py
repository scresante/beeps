import pulseio
import board
import adafruit_irremote
from adafruit_circuitplayground.express import cpx
from ir_codes import decode_ir

# Create a 'pulseio' input, to listen to infrared signals on the IR receiver
pulsein = pulseio.PulseIn(board.IR_RX, maxlen=120, idle_state=True)
# Create a decoder that will take pulses and turn them into numbers
decoder = adafruit_irremote.GenericDecode()

while True:
    try:
        pulses = decoder.read_pulses(pulsein)
        # Attempt to convert received pulses into numbers
        received_code = decoder.decode_bits(pulses, debug=False)
    except adafruit_irremote.IRNECRepeatException:
        # We got an unusual short code, probably a 'repeat' signal
        # print("NEC repeat!")
        continue
    except adafruit_irremote.IRDecodeException as e:
        # Something got distorted or maybe its not an NEC-type remote?
        # print("Failed to decode: ", e.args)
        continue
    try:
        print("received %s :: %s" % (received_code, decode_ir(received_code)))
        cpx.play_tone(received_code[2], 1)
    except KeyError as e:
        print("received unknown signal: %s" % e)

