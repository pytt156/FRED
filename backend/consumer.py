import json

import paho.mqtt.client as mqtt
from state_manager import handle_message


def on_message(client, userdata, message):
    payload = message.payload.decode()
    data = json.loads(payload)

    handle_message(client, message.topic, data)


if __name__ == "__main__":
    client = mqtt.Client()
    client.connect("localhost", 1883)

    client.subscribe("fred/room/metrics")
    client.subscribe("fred/room/light")
    client.subscribe("fred/room/noise")
    client.subscribe("fred/network/status")

    client.on_message = on_message
    client.loop_forever()
