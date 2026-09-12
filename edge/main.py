from wifi import connect_wifi
from machine import Pin
import time
from dht11 import read_dht11
from light_sensor import read_light
from motion_sensor import read_motion

time.sleep(.5)

led = Pin(14, Pin.OUT)
led.value(0)

if connect_wifi():
    led.value(1)

while True:
    dht_data = read_dht11()
    light_data = read_light()
    motion_data = read_motion()

    time.sleep(1)