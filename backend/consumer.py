import json
import paho.mqtt.client as mqtt

from backend.room_state import evaluate_room_state


def on_message(client, userdata, message):
    payload = message.payload.decode()
    data = json.loads(payload)

    print(message.topic, data)

    if message.topic == "fred/room/metrics":
        temperature = float(data["data"]["temperature"])
        humidity = float(data["data"]["humidity"])

        room_state = evaluate_room_state(temperature, humidity)

        print(f"room state: {room_state}")


if __name__ == "__main__":
    client = mqtt.Client()
    client.connect("localhost", 1883)
    client.subscribe("fred/room/metrics")
    client.subscribe("fred/network/status")
    client.on_message = on_message
    client.loop_forever()
