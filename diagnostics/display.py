from machine import Pin, I2C

i2c = I2C(
    0,
    sda=Pin(4),
    scl=Pin(5),
    freq=400000
)

print(i2c.scan())