from wifi import connect_wifi
from machine import Pin
import time

from dht11 import read_dht11
from light_sensor import read_light
from motion_sensor import read_motion
from network_metrics import read_network_metrics
from display import show_fred_face, show_room_status, show_network_status
from button import read_button
from speaker import play_tone
from interaction_button import read_interaction_button

from mqtt_client import connect_mqtt, publish_room_metrics, publish_light, publish_motion, publish_network_status, publish_interaction_button

SCREEN_FRED = 0
SCREEN_ROOM = 1
SCREEN_NETWORK = 2

current_screen = SCREEN_FRED    

time.sleep(.5)

led = Pin(14, Pin.OUT)
led.value(0)

wifi_connected = connect_wifi()

mqtt_connected = False

if wifi_connected:
    led.value(1)
    mqtt_connected = connect_mqtt()

last_button_pressed = False
last_interaction_button_pressed = False


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
        current_screen += 1

        if current_screen > SCREEN_NETWORK:
            current_screen = SCREEN_FRED

        play_tone(frequency=700, duration=0.1)


    last_button_pressed = button_pressed

    interaction_button_data = read_interaction_button()
    interaction_button_pressed = interaction_button_data["pressed"]

    if (
        interaction_button_pressed
        and not last_interaction_button_pressed
        and mqtt_connected
    ):
        publish_interaction_button()

    last_interaction_button_pressed = interaction_button_pressed
    
    if current_screen == SCREEN_FRED:
        show_fred_face("happy")

    elif current_screen == SCREEN_ROOM:
        show_room_status(
            dht_data["temperature"],
            dht_data["humidity"],
            light_data["light"],
            motion_data["motion"],
        )

    elif current_screen == SCREEN_NETWORK:
        show_network_status(
            network_data["connected"],
            network_data["rssi"],
            mqtt_connected
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