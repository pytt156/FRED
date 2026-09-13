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


def clear_display():
    display.fill(0)


def draw_happy_face():
    clear_display()

    # Eyes
    display.fill_rect(30, 20, 10, 10, 1)
    display.fill_rect(88, 20, 10, 10, 1)

    # Smile
    display.line(46, 42, 54, 48, 1)
    display.line(54, 48, 64, 51, 1)
    display.line(64, 51, 74, 48, 1)
    display.line(74, 48, 82, 42, 1)

    display.show()


def draw_grumpy_face():
    clear_display()

    # Eyes
    display.line(28, 19, 42, 24, 1)
    display.line(86, 24, 100, 19, 1)

    display.fill_rect(32, 26, 8, 8, 1)
    display.fill_rect(88, 26, 8, 8, 1)

    # Mouth
    display.line(48, 50, 58, 45, 1)
    display.line(58, 45, 70, 45, 1)
    display.line(70, 45, 80, 50, 1)

    display.show()


def draw_sleepy_face():
    clear_display()

    # Closed eyes
    display.line(28, 28, 42, 28, 1)
    display.line(86, 28, 100, 28, 1)

    # Small mouth
    display.line(57, 47, 71, 47, 1)

    # Sleep indicator
    display.text("z", 103, 10)
    display.text("Z", 112, 2)

    display.show()


def draw_uncomfortable_face():
    clear_display()

    # Eyes
    display.fill_rect(30, 23, 9, 9, 1)
    display.fill_rect(89, 23, 9, 9, 1)

    # Uneasy mouth
    display.line(48, 48, 55, 44, 1)
    display.line(55, 44, 62, 48, 1)
    display.line(62, 48, 69, 44, 1)
    display.line(69, 44, 77, 48, 1)

    display.show()


def draw_disconnected_face():
    clear_display()

    # X eyes
    display.line(29, 22, 40, 33, 1)
    display.line(40, 22, 29, 33, 1)

    display.line(88, 22, 99, 33, 1)
    display.line(99, 22, 88, 33, 1)

    # Flat mouth
    display.line(52, 48, 76, 48, 1)

    display.show()


def show_fred_face(face="happy"):
    if face == "happy":
        draw_happy_face()

    elif face == "grumpy":
        draw_grumpy_face()

    elif face == "sleepy":
        draw_sleepy_face()

    elif face == "uncomfortable":
        draw_uncomfortable_face()

    elif face == "disconnected":
        draw_disconnected_face()

    else:
        draw_happy_face()


def show_room_status(
    temperature,
    humidity,
    light,
    motion
):
    clear_display()

    display.text("ROOM", 0, 0)

    display.text(
        "Temp: " + str(temperature) + " C",
        0,
        16
    )

    display.text(
        "Hum:  " + str(humidity) + " %",
        0,
        28
    )

    display.text(
        "Light: " + str(light),
        0,
        40
    )

    if motion:
        motion_text = "YES"
    else:
        motion_text = "NO"

    display.text(
        "Motion: " + motion_text,
        0,
        52
    )

    display.show()


def show_network_status(
    connected,
    rssi,
    mqtt_connected
):
    clear_display()

    display.text("NETWORK", 0, 0)

    if connected:
        display.text(
            "WiFi: ONLINE",
            0,
            18
        )
    else:
        display.text(
            "WiFi: OFFLINE",
            0,
            18
        )

    if rssi is not None:
        display.text(
            "RSSI: " + str(rssi),
            0,
            34
        )
    else:
        display.text(
            "RSSI: N/A",
            0,
            34
        )

    if mqtt_connected:
        display.text(
            "MQTT: ONLINE",
            0,
            50
        )
    else:
        display.text(
            "MQTT: OFFLINE",
            0,
            50
        )

    display.show()