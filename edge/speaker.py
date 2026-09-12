from machine import Pin, I2S
from array import array
import math
import time


SAMPLE_RATE = 16000


def play_tone(frequency=440, duration=0.2, amplitude=5000):
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

    number_of_samples = int(
        SAMPLE_RATE * duration
    )

    for i in range(number_of_samples):
        sample = int(
            amplitude *
            math.sin(
                2 * math.pi *
                frequency *
                i /
                SAMPLE_RATE
            )
        )

        samples.append(sample)
        samples.append(sample)

    audio.write(samples)

    time.sleep(duration)

    audio.deinit()