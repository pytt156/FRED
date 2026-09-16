import json
import os

import paho.mqtt.client as mqtt

from state_manager import handle_message


MQTT_HOST = os.getenv("MQTT_HOST", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
MQTT_USERNAME = os.getenv("MQTT_USERNAME")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")

def on_message(client, userdata, message):
    payload = message.payload.decode()
    data = json.loads(payload)

    handle_message(client, message.topic, data)


if __name__ == "__main__":
    client = mqtt.Client()

    if MQTT_USERNAME and MQTT_PASSWORD:
        client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    elif MQTT_USERNAME or MQTT_PASSWORD:
        raise ValueError("MQTT_USERNAME AND MQTT_PASSWORD must both be configured")

    client.on_message = on_message

    client.connect(MQTT_HOST, MQTT_PORT)
    
    client.subscribe("fred/room/metrics")
    client.subscribe("fred/room/light")
    client.subscribe("fred/room/noise")
    client.subscribe("fred/room/motion")
    client.subscribe("fred/network/status")
    client.subscribe("fred/interaction/button")

    print("FRED consumer connected to MQTT broker:",MQTT_HOST,MQTT_PORT, flush=True)

    client.loop_forever()
