from array import array
import math
import time

from machine import I2S, Pin


TONE_SAMPLE_RATE = 16000

audio = None


def play_tone(
    frequency=440,
    duration=0.2,
    amplitude=5000,
):
    tone_audio = I2S(
        0,
        sck=Pin(10),
        ws=Pin(11),
        sd=Pin(9),
        mode=I2S.TX,
        bits=16,
        format=I2S.STEREO,
        rate=TONE_SAMPLE_RATE,
        ibuf=20000,
    )

    samples = array("h")

    number_of_samples = int(TONE_SAMPLE_RATE * duration)

    for i in range(number_of_samples):
        sample = int(
            amplitude * math.sin(2 * math.pi * frequency * i / TONE_SAMPLE_RATE)
        )

        samples.append(sample)
        samples.append(sample)

    tone_audio.write(samples)

    time.sleep(duration)

    tone_audio.deinit()


def start_audio(sample_rate=24000):
    global audio

    if audio is not None:
        audio.deinit()

    audio = I2S(
        0,
        sck=Pin(10),
        ws=Pin(11),
        sd=Pin(9),
        mode=I2S.TX,
        bits=16,
        format=I2S.MONO,
        rate=sample_rate,
        ibuf=20000,
    )


def write_audio_chunk(data):
    if audio is not None:
        audio.write(data)


def stop_audio():
    global audio

    if audio is not None:
        audio.deinit()
        audio = None
