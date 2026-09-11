import json

import paho.mqtt.client as mqtt
from fred_state import evaluate_fred_state, get_display_state
from network_state import evaluate_network_state
from room_state import evaluate_room_state

latest_room_data = {
    "temperature": None,
    "humidity": None,
    "light": None,
    "noise": None,
}

latest_network_data = {
    "connected": None,
    "rssi": None,
    "latency_ms": None,
}

last_room_state = None
last_fred_states = None
last_display_state = None


def on_message(client, userdata, message):
    global last_room_state, last_fred_states, last_display_state

    payload = message.payload.decode()
    data = json.loads(payload)

    print(message.topic, data)

    if message.topic == "fred/room/metrics":
        latest_room_data["temperature"] = data["data"].get("temperature")
        latest_room_data["humidity"] = data["data"].get("humidity")

    elif message.topic == "fred/network/status":
        latest_network_data["connected"] = data["data"].get("connected")
        latest_network_data["rssi"] = data["data"].get("rssi")
        latest_network_data["latency_ms"] = data["data"].get("latency_ms")

    elif message.topic == "fred/room/light":
        latest_room_data["light"] = data["data"].get("light")

    elif message.topic == "fred/room/noise":
        latest_room_data["noise"] = data["data"].get("noise")

    room_conditions = evaluate_room_state(
        temperature=latest_room_data["temperature"],
        humidity=latest_room_data["humidity"],
        light=latest_room_data["light"],
        noise=latest_room_data["noise"],
    )

    network_conditions = evaluate_network_state(
        connected=latest_network_data["connected"],
        rssi=latest_network_data["rssi"],
        latency_ms=latest_network_data["latency_ms"],
    )

    if "OFFLINE" in network_conditions:
        room_state = ["OFFLINE"]
    else:
        room_state = room_conditions + network_conditions

    fred_states = evaluate_fred_state(room_state)
    display_state = get_display_state(fred_states)

    if room_state != last_room_state:
        print(f"room state changed: {room_state}")
        last_room_state = room_state

    if fred_states != last_fred_states:
        print(f"fred states changed: {fred_states}")
        last_fred_states = fred_states

    if display_state != last_display_state:
        print(f"display state changed: {display_state}")
        last_display_state = display_state


if __name__ == "__main__":
    client = mqtt.Client()
    client.connect("localhost", 1883)
    client.subscribe("fred/room/metrics")
    client.subscribe("fred/room/light")
    client.subscribe("fred/room/noise")
    client.subscribe("fred/network/status")
    client.on_message = on_message
    client.loop_forever()
