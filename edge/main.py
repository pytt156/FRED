from wifi import connect_wifi
from machine import Pin
import time
from dht11 import read_dht11

time.sleep(.5)

led = Pin(14, Pin.OUT)
led.value(0)

if connect_wifi():
    led.value(1)

while True:
    dht_data = read_dht11()
    time.sleep(1)