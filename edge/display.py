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


def show_status(temperature, humidity, light, motion, connected, rssi):
    display.fill(0)

    display.text("FRED", 0, 0)

    display.text(
        "T:" + str(temperature) + "C H:" + str(humidity) + "%",
        0,
        14
    )

    display.text(
        "Light:" + str(light),
        0,
        26
    )

    display.text(
        "Motion:" + str(motion),
        0,
        38
    )

    if connected:
        display.text(
            "WiFi:" + str(rssi),
            0,
            50
        )
    else:
        display.text(
            "WiFi: OFFLINE",
            0,
            50
        )

    display.show()