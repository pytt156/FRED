import json
import time


def publish_room_state(client, room_state):
    payload = {
        "timestamp": time.time(),
        "source": "derived",
        "data": {
            "states": room_state,
        },
    }

    client.publish("fred/state/room", json.dumps(payload))


def publish_fred_state(client, fred_states, display_state):
    payload = {
        "timestamp": time.time(),
        "source": "derived",
        "data": {
            "states": fred_states,
            "display_state": display_state,
        },
    }

    client.publish("fred/state/fred", json.dumps(payload))
