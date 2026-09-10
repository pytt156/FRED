from wifi import connect_wifi
from machine import Pin
from dht import DHT11
import time

time.sleep(.5)

led = Pin(14, Pin.OUT)
led.value(0)

if connect_wifi():
    led.value(1)

