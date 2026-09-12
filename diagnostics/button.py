from machine import Pin
import time

button = Pin(
    16,
    Pin.IN,
    Pin.PULL_UP
)

while True:
    print(button.value())
    time.sleep(0.2)