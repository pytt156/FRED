from machine import Pin


button = Pin(
    16,
    Pin.IN,
    Pin.PULL_UP
)


def read_button():
    pressed = button.value() == 0

    button_data = {
        "pressed": pressed
    }

    print(button_data)

    return button_data