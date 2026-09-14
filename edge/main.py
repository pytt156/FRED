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

from mqtt_client import connect_mqtt, publish_room_metrics, publish_light, publish_motion, publish_network_status

time.sleep(.5)

led = Pin(14, Pin.OUT)
led.value(0)

wifi_connected = connect_wifi()

mqtt_connected = False

if wifi_connected:
    led.value(1)
    mqtt_connected = connect_mqtt()

last_button_pressed = False


while True:
    network_data = read_network_metrics()

    if not network_data["connected"]:
        print("Wifi disconnected")

        led.value(0)
        mqtt_connected = False

        print("Attempting wifi reconnect..")

        wifi_connected = connect_wifi()

        if wifi_connected:
            print("Wifi reconnected")

            led.value(1)
            network_data = read_network_metrics()
    else: 
        led.value(1)

    if network_data["connected"] and not mqtt_connected:
        print("Attempting MQTT reconnect..")

        mqtt_connected = connect_mqtt()

    dht_data = read_dht11()
    light_data = read_light()
    motion_data = read_motion()
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


    if mqtt_connected:
        metrics_published = publish_room_metrics(dht_data["temperature"], dht_data["humidity"])
        light_published = publish_light(light_data["light"])
        motion_published = publish_motion(motion_data["motion"])
        network_published = publish_network_status(network_data["connected"], network_data["rssi"])


        if not (metrics_published and light_published and motion_published and network_published):
            print("MQTT connection lost")
            mqtt_connected = False
        
    time.sleep(1)