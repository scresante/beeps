import adafruit_irremote

def get_ir(decoder, pulsein):
    ircodes = {
        "[255, 2, 255, 0]": "vol-",
        "[255, 2, 127, 128]": "play",
        "[255, 2, 191, 64]": "vol+",
        "[255, 2, 223, 32]": "setup",
        "[255, 2, 159, 96]": "mode",
        "[255, 2, 207, 48]": "0_10+",
        "[255, 2, 143, 112]": "return",
        "[255, 2, 95, 160]": "up",
        "[255, 2, 79, 176]": "down",
        "[255, 2, 239, 16]": "left",
        "[255, 2, 175, 80]": "right",
        "[255, 2, 111, 144]": "enter",
        "[255, 2, 247, 8]": "1",
        "[255, 2, 119, 136]": "2",
        "[255, 2, 183, 72]": "3",
        "[255, 2, 215, 40]": "4",
        "[255, 2, 87, 168]": "5",
        "[255, 2, 151, 104]": "6",
        "[255, 2, 231, 24]": "7",
        "[255, 2, 103, 152]": "8",
        "[255, 2, 167, 88]": "9",
    }

    try:
        pulses = decoder.read_pulses(pulsein)
        # Attempt to convert received pulses into numbers
        received_code = decoder.decode_bits(pulses, debug=False)
    except adafruit_irremote.IRNECRepeatException:
        # We got an unusual short code, probably a 'repeat' signal
        # print("NEC repeat!")
        pass
    except adafruit_irremote.IRDecodeException as e:
        # Something got distorted or maybe its not an NEC-type remote?
        # print("Failed to decode: ", e.args)
        pass
    try:
        # print("received %s " % (received_code))
        return ircodes[str(received_code)]
    except KeyError as e:
        print("received unknown signal: %s" % e)
    except NameError as e:
        print("encountered a NameError: %s" % e)



