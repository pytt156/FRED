from machine import Pin


button = Pin(
    16,
    Pin.IN,
    Pin.PULL_UP
)


def read_button():
    return {
        "pressed": button.value() == 0
    }