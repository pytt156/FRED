from wifi import connect_wifi
from machine import Pin
import time
from dht11 import read_dht11
from light_sensor import read_light
from motion_sensor import read_motion
from network_metrics import read_network_metrics
from display import show_status

time.sleep(.5)

led = Pin(14, Pin.OUT)
led.value(0)

if connect_wifi():
    led.value(1)

while True:
    dht_data = read_dht11()
    light_data = read_light()
    motion_data = read_motion()
    network_data = read_network_metrics()
    show_status(
        dht_data["temperature"],
        dht_data["humidity"],
        light_data["light"],
        motion_data["motion"],
        network_data["connected"],
        network_data["rssi"]
    )    

    time.sleep(1)