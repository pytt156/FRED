from simple import MQTTClient
from speaker import start_audio, write_audio_chunk, stop_audio
from device_config import(
    DEPLOYMENT,
    LOCAL_MQTT_HOST,
    LOCAL_MQTT_PORT,
    AZURE_MQTT_HOST,
    AZURE_MQTT_PORT
)

import json
import time
import ssl

CLIENT_ID = "fred-pico-01"

ROOM_METRICS_TOPIC = b"fred/room/metrics"
LIGHT_TOPIC = b"fred/room/light"
MOTION_TOPIC = b"fred/room/motion"
NETWORK_STATUS_TOPIC = b"fred/network/status"
INTERACTION_BUTTON_TOPIC = b"fred/interaction/button"
AUDIO_START_TOPIC = b"fred/audio/start"
AUDIO_CHUNK_TOPIC = b"fred/audio/chunk"
AUDIO_END_TOPIC = b"fred/audio/end"

FRED_STATE_TOPIC = b"fred/state/fred"

client = None
fred_display_state = "HAPPY"
audio_receiving = False

def create_mqtt_client():
    if DEPLOYMENT == "local":
        print("MQTT deployment: local")
        print("MQTT broker:", LOCAL_MQTT_HOST, LOCAL_MQTT_PORT)

        return MQTTClient(CLIENT_ID, LOCAL_MQTT_HOST, port=LOCAL_MQTT_PORT)


    if DEPLOYMENT == "azure":
        from mqtt_azure_creds import MQTT_USERNAME, MQTT_PASSWORD

        if not AZURE_MQTT_HOST:
            raise ValueError("AZURE_MQTT_HOST is not configured in device_config.py")

        if not MQTT_USERNAME or not MQTT_PASSWORD:
            raise ValueError("Azure MQTT username/password are not configured in mqtt_azure_creds.py")

        print("MQTT deployment: azure")
        print("MQTT broker:", AZURE_MQTT_HOST, AZURE_MQTT_PORT)
        print("MQTT TLS: enabled")

        tls_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        tls_context.verify_mode = ssl.CERT_REQUIRED
        tls_context.load_verify_locations("fred-ca.crt")

        return MQTTClient(
            CLIENT_ID,
            AZURE_MQTT_HOST, 
            port=AZURE_MQTT_PORT,
            user=MQTT_USERNAME,
            password=MQTT_PASSWORD,
            ssl=tls_context
        )

    raise ValueError("Invalid DEPLOYMENT in device_config.py: {}".format(DEPLOYMENT))

def on_mqtt_message(topic, message):
    global fred_display_state, audio_receiving

    if topic == AUDIO_START_TOPIC:
        metadata = json.loads(message.decode())

        print("Audio start:", metadata)

        start_audio(metadata["sample_rate"])
        audio_receiving = True
        return

    if topic == AUDIO_CHUNK_TOPIC:
        write_audio_chunk(message)
        return

    if topic == AUDIO_END_TOPIC:
        print("Audio end")

        stop_audio()
        audio_receiving = False
        return

    try:
        data = json.loads(message.decode())
        print("MQTT received:", topic, data)

        if topic == FRED_STATE_TOPIC:
            display_state = data["data"]["display_state"]

            fred_display_state = display_state
            print("FRED display state:", fred_display_state)

    except Exception as error:
        print("MQTT message error:", error)


def connect_mqtt():
    global client

    try:
        client = create_mqtt_client()
        client.set_callback(on_mqtt_message)
        client.connect()
        client.subscribe(FRED_STATE_TOPIC)
        client.subscribe(AUDIO_START_TOPIC)
        client.subscribe(AUDIO_CHUNK_TOPIC)
        client.subscribe(AUDIO_END_TOPIC)

        print("MQTT connected")
        print("Subscribed to:", FRED_STATE_TOPIC)

        return True

    except Exception as error:
        print("MQTT connection failed:", error)
        return False


def check_mqtt_messages():
    global audio_receiving

    try:
        client.check_msg()

        if audio_receiving:
            started_at = time.ticks_ms()
            timeout_ms = 15000

            while audio_receiving:
                client.check_msg()

                if time.ticks_diff(time.ticks_ms(), started_at) > timeout_ms:
                    print("Audio receive timed out")
                    stop_audio()
                    audio_receiving = False
                    break

                time.sleep_ms(1)

        return True

    except Exception as error:
        print("MQTT receive failed:", error)

        if audio_receiving:
            stop_audio()
            audio_receiving = False

        return False


def get_fred_display_state():
    return fred_display_state


def publish_interaction_button():
    payload = {"timestamp": time.time(), "source": "real", "data": {"pressed": True}}

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
        "data": {"temperature": temperature, "humidity": humidity},
    }

    return publish_json(ROOM_METRICS_TOPIC, payload)


def publish_light(light):
    payload = {"timestamp": time.time(), "source": "real", "data": {"light": light}}

    return publish_json(LIGHT_TOPIC, payload)


def publish_motion(motion):
    payload = {"timestamp": time.time(), "source": "real", "data": {"motion": motion}}

    return publish_json(MOTION_TOPIC, payload)


def publish_network_status(connected, rssi):
    payload = {
        "timestamp": time.time(),
        "source": "real",
        "data": {"connected": connected, "rssi": rssi},
    }

    return publish_json(NETWORK_STATUS_TOPIC, payload)
