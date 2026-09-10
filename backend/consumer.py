import json

import paho.mqtt.client as mqtt
from room_state import evaluate_room_state

latest_room_data = {
    "temperature": None,
    "humidity": None,
    "light": None,
    "noise": None,
}


def on_message(client, userdata, message):
    payload = message.payload.decode()
    data = json.loads(payload)

    print(message.topic, data)

    if message.topic == "fred/room/metrics":
        latest_room_data["temperature"] = data["data"].get("temperature")
        latest_room_data["humidity"] = data["data"].get("humidity")

    elif message.topic == "fred/room/light":
        latest_room_data["light"] = data["data"].get("light")

    elif message.topic == "fred/room/noise":
        latest_room_data["noise"] = data["data"].get("noise")

    room_state = evaluate_room_state(
        temperature=latest_room_data["temperature"],
        humidity=latest_room_data["humidity"],
        light=latest_room_data["light"],
        noise=latest_room_data["noise"],
    )

    print(f"room state: {room_state}")


if __name__ == "__main__":
    client = mqtt.Client()
    client.connect("localhost", 1883)
    client.subscribe("fred/room/metrics")
    client.subscribe("fred/network/status")
    client.on_message = on_message
    client.loop_forever()
