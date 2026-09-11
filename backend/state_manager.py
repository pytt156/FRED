from fred_state import evaluate_fred_state, get_display_state
from network_state import evaluate_network_state
from publisher import publish_fred_state, publish_room_state
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


def handle_message(client, topic, data):
    global last_room_state, last_fred_states, last_display_state

    if topic == "fred/room/metrics":
        latest_room_data["temperature"] = data["data"].get("temperature")
        latest_room_data["humidity"] = data["data"].get("humidity")

    elif topic == "fred/room/light":
        latest_room_data["light"] = data["data"].get("light")

    elif topic == "fred/room/noise":
        latest_room_data["noise"] = data["data"].get("noise")

    elif topic == "fred/network/status":
        latest_network_data["connected"] = data["data"].get("connected")
        latest_network_data["rssi"] = data["data"].get("rssi")
        latest_network_data["latency_ms"] = data["data"].get("latency_ms")

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

    fred_changed = fred_states != last_fred_states
    display_changed = display_state != last_display_state

    if room_state != last_room_state:
        print(f"room state changed: {room_state}")
        publish_room_state(client, room_state)
        last_room_state = room_state

    if fred_changed:
        print(f"fred states changed: {fred_states}")
        last_fred_states = fred_states

    if display_changed:
        print(f"display state changed: {display_state}")
        last_display_state = display_state

    if fred_changed or display_changed:
        publish_fred_state(client, fred_states, display_state)
