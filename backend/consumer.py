import json
import os

import paho.mqtt.client as mqtt

from state_manager import handle_message


MQTT_HOST = os.getenv("MQTT_HOST", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))

def on_message(client, userdata, message):
    payload = message.payload.decode()
    data = json.loads(payload)

    handle_message(client, message.topic, data)


if __name__ == "__main__":
    client = mqtt.Client()
    client.connect(MQTT_HOST, MQTT_PORT)

    client.subscribe("fred/room/metrics")
    client.subscribe("fred/room/light")
    client.subscribe("fred/room/noise")
    client.subscribe("fred/room/motion")
    client.subscribe("fred/network/status")
    client.subscribe("fred/interaction/button")

    client.on_message = on_message
    print("FRED consumer connected to MQTT broker:",MQTT_HOST,MQTT_PORT,)
    client.loop_forever()
