from wifi import connect_wifi
from machine import Pin
import time

from dht11 import read_dht11
from light_sensor import read_light
from motion_sensor import read_motion
from network_metrics import read_network_metrics
from display import show_status
from button import read_button
from speaker import play_tone


time.sleep(.5)

led = Pin(14, Pin.OUT)
led.value(0)

if connect_wifi():
    led.value(1)


last_button_pressed = False


while True:
    dht_data = read_dht11()

    light_data = read_light()

    motion_data = read_motion()

    network_data = read_network_metrics()

    button_data = read_button()

    button_pressed = button_data["pressed"]

    if button_pressed and not last_button_pressed:
        play_tone(
            frequency=700,
            duration=0.1
        )

    last_button_pressed = button_pressed

    show_status(
        dht_data["temperature"],
        dht_data["humidity"],
        light_data["light"],
        motion_data["motion"],
        network_data["connected"],
        network_data["rssi"]
    )

    time.sleep(1)