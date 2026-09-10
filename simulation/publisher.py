import json
import random
import time

import paho.mqtt.client as mqtt

BROKER_HOST = "localhost"
BROKER_PORT = 1883

ROOM_METRICS_TOPIC = "fred/room/metrics"
NETWORK_STATUS_TOPIC = "fred/network/status"
LIGHT_TOPIC = "fred/room/light"
NOISE_TOPIC = "fred/room/noise"

client = mqtt.Client()
client.connect(BROKER_HOST, BROKER_PORT)

while True:
    room_data = {
        "timestamp": time.time(),
        "source": "simulated",
        "data": {
            "temperature": round(random.uniform(20.0, 26.0), 1),
            "humidity": round(random.uniform(35.0, 55.0), 1),
        },
    }

    network_data = {
        "timestamp": time.time(),
        "source": "simulated",
        "data": {
            "rssi": random.randint(-75, -45),
            "latency_ms": random.randint(15, 80),
        },
    }

    light_data = {
        "timestamp": time.time(),
        "source": "simulated",
        "data": {
            "light": random.randint(0, 65535),
        },
    }

    noise_data = {
        "timestamp": time.time(),
        "source": "simulated",
        "data": {
            "noise": random.randint(0, 100),
        },
    }

    client.publish(ROOM_METRICS_TOPIC, json.dumps(room_data))
    client.publish(NETWORK_STATUS_TOPIC, json.dumps(network_data))
    client.publish(LIGHT_TOPIC, json.dumps(light_data))
    client.publish(NOISE_TOPIC, json.dumps(noise_data))

    print(f"sent room metrics: {room_data}, {light_data}, {noise_data}")
    print(f"sent network status: {network_data}")

    time.sleep(3)
