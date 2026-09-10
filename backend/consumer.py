import json

import paho.mqtt.client as mqtt


def on_message(client, userdata, message):
    payload = message.payload.decode()
    data = json.loads(payload)

    print(data)


if __name__ == "__main__":
    client = mqtt.Client()
    client.connect("localhost", 1883)
    client.subscribe("fred/room/metrics")
    client.on_message = on_message
    client.loop_forever()
