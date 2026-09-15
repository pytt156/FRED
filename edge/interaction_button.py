from machine import Pin

INTERACTION_BUTTON_PIN = 17

button = Pin(
    INTERACTION_BUTTON_PIN,
    Pin.IN,
    Pin.PULL_UP,
)


def read_interaction_button():
    return {
        "pressed": button.value() == 0
    }