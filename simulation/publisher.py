import json
import time

import paho.mqtt.client as mqtt
from scenarios import SCENARIOS, random_scenario

BROKER_HOST = "localhost"
BROKER_PORT = 1883

ROOM_METRICS_TOPIC = "fred/room/metrics"
NETWORK_STATUS_TOPIC = "fred/network/status"
LIGHT_TOPIC = "fred/room/light"
NOISE_TOPIC = "fred/room/noise"

SCENARIO = "dark"

client = mqtt.Client()
client.connect(BROKER_HOST, BROKER_PORT)


while True:
    if SCENARIO == "random":
        scenario = random_scenario()
    else:
        scenario = SCENARIOS[SCENARIO]

    room_data = {
        "timestamp": time.time(),
        "source": "simulated",
        "data": {
            "temperature": scenario["temperature"],
            "humidity": scenario["humidity"],
        },
    }

    network_data = {
        "timestamp": time.time(),
        "source": "simulated",
        "data": {
            "connected": scenario["connected"],
            "rssi": scenario["rssi"],
            "latency_ms": scenario["latency_ms"],
        },
    }

    light_data = {
        "timestamp": time.time(),
        "source": "simulated",
        "data": {
            "light": scenario["light"],
        },
    }

    noise_data = {
        "timestamp": time.time(),
        "source": "simulated",
        "data": {
            "noise": scenario["noise"],
        },
    }

    client.publish(ROOM_METRICS_TOPIC, json.dumps(room_data))
    client.publish(NETWORK_STATUS_TOPIC, json.dumps(network_data))
    client.publish(LIGHT_TOPIC, json.dumps(light_data))
    client.publish(NOISE_TOPIC, json.dumps(noise_data))

    print(f"sent room metrics: {room_data}, {light_data}, {noise_data}")
    print(f"sent network status: {network_data}")

    time.sleep(3)
