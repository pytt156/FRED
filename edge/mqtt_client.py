from simple import MQTTClient
import json
import time

BROKER_IP = "172.20.10.4"
BROKER_PORT = 1883
CLIENT_ID = "fred-pico-01"

ROOM_METRICS_TOPIC = b"fred/room/metrics"
LIGHT_TOPIC = b"fred/room/light"
MOTION_TOPIC = b"fred/room/motion"
NETWORK_STATUS_TOPIC = b"fred/network/status"
INTERACTION_BUTTON_TOPIC = b"fred/interaction/button"

client = None

def connect_mqtt():
    global client

    try:
        client = MQTTClient(CLIENT_ID, BROKER_IP, port=BROKER_PORT)
        client.connect()
        print("MQTT connected")
        return True
    except Exception as error:
        print("MQTT connection failed:", error)
        return False


def publish_interaction_button():
    payload = {
        "timestamp": time.time(),
        "source": "real",
        "data": {"pressed": True}
    }

    return publish_json(INTERACTION_BUTTON_TOPIC, payload)

def publish_json(topic, data):
    try: 
        payload = json.dumps(data)
        client.publish(topic, payload.encode())
        print("MQTT published:", topic, payload)
        return True

    except Exception as error:
        print("MQTT publish failed:", error)
        return False


def publish_room_metrics(temperature, humidity):
    payload = {
        "timestamp": time.time(),
        "source": "real",
        "data": {
            "temperature": temperature,
            "humidity": humidity
        }
    }

    return publish_json(ROOM_METRICS_TOPIC, payload)


def publish_light(light):
    payload = {
        "timestamp": time.time(),
        "source": "real",
        "data": {
            "light": light
        }
    }

    return publish_json(LIGHT_TOPIC, payload)


def publish_motion(motion):
    payload = {
        "timestamp": time.time(),
        "source": "real",
        "data": {
            "motion": motion
        }
    }

    return publish_json(MOTION_TOPIC, payload)


def publish_network_status(connected, rssi):
    payload = {
        "timestamp": time.time(),
        "source": "real",
        "data": {
            "connected": connected,
            "rssi": rssi
        }
    }

    return publish_json(NETWORK_STATUS_TOPIC, payload)

