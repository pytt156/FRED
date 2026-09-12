from machine import Pin, I2S
from array import array
import math
import time


SAMPLE_RATE = 16000
FREQUENCY = 440
DURATION = 1
AMPLITUDE = 5000


audio = I2S(
    0,
    sck=Pin(10),
    ws=Pin(11),
    sd=Pin(9),
    mode=I2S.TX,
    bits=16,
    format=I2S.STEREO,
    rate=SAMPLE_RATE,
    ibuf=20000
)


samples = array("h")

number_of_samples = SAMPLE_RATE * DURATION

for i in range(number_of_samples):
    sample = int(
        AMPLITUDE *
        math.sin(
            2 * math.pi *
            FREQUENCY *
            i /
            SAMPLE_RATE
        )
    )

    # Same tone in left and right channels
    samples.append(sample)
    samples.append(sample)


print("Playing tone...")

audio.write(samples)

time.sleep(1)

audio.deinit()

print("Done")