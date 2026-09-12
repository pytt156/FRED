from machine import Pin, I2C
import sh1106

i2c = I2C(
    0,
    sda=Pin(4),
    scl=Pin(5),
    freq=400000
)

oled = sh1106.SH1106_I2C(
    128,
    64,
    i2c
)

oled.fill(0)

oled.text("FRED", 0, 0)
oled.text("OLED working", 0, 20)

oled.show()