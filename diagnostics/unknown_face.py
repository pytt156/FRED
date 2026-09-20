from machine import Pin, I2C
import sh1106

i2c = I2C(
    0,
    sda=Pin(4),
    scl=Pin(5),
    freq=400000
)

display = sh1106.SH1106_I2C(
    128,
    64,
    i2c
)

def draw_question_mark(x, y):
    # Hook
    display.line(x, y, x + 6, y, 1)
    display.line(x + 6, y, x + 8, y + 3, 1)
    display.line(x + 8, y + 3, x + 5, y + 6, 1)
    display.line(x + 5, y + 6, x + 5, y + 8, 1)

    # Dot
    display.fill_rect(x + 3, y + 11, 3, 3, 1)


def draw_unknown_face():

    # Question mark eyes
    draw_question_mark(28, 16)
    draw_question_mark(86, 16)

    # Uncertain, wavy mouth
    display.line(44, 50, 54, 42, 1)
    display.line(54, 42, 64, 50, 1)
    display.line(64, 50, 74, 42, 1)
    display.line(74, 42, 84, 50, 1)

    display.show()

draw_unknown_face()