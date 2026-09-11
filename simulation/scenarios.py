import random

SCENARIOS = {
    "healthy": {
        "temperature": 22.0,
        "humidity": 45.0,
        "light": 50000,
        "noise": 30,
        "connected": True,
        "rssi": -55,
        "latency_ms": 50,
    },
    "hot": {
        "temperature": 29.0,
        "humidity": 45.0,
        "light": 50000,
        "noise": 30,
        "connected": True,
        "rssi": -55,
        "latency_ms": 50,
    },
    "dark": {
        "temperature": 22.0,
        "humidity": 45.0,
        "light": 10000,
        "noise": 30,
        "connected": True,
        "rssi": -55,
        "latency_ms": 50,
    },
    "noisy": {
        "temperature": 22.0,
        "humidity": 45.0,
        "light": 50000,
        "noise": 90,
        "connected": True,
        "rssi": -55,
        "latency_ms": 50,
    },
    "bad_network": {
        "temperature": 22.0,
        "humidity": 45.0,
        "light": 50000,
        "noise": 30,
        "connected": True,
        "rssi": -75,
        "latency_ms": 180,
    },
    "offline": {
        "temperature": 22.0,
        "humidity": 45.0,
        "light": 50000,
        "noise": 30,
        "connected": False,
        "rssi": -55,
        "latency_ms": 50,
    },
}


def random_scenario():
    return {
        "temperature": round(random.uniform(20.0, 26.0), 1),
        "humidity": round(random.uniform(35.0, 55.0), 1),
        "light": random.randint(0, 65535),
        "noise": random.randint(0, 100),
        "connected": random.choice([True, True, True, False]),
        "rssi": random.randint(-75, -45),
        "latency_ms": random.randint(15, 180),
    }
