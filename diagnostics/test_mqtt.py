import time

from mqtt_client import connect_mqtt, publish_json
from wifi import connect_wifi

if connect_wifi() and connect_mqtt():
    publish_json(
        b"fred/test",
        {
            "timestamp": time.time(),
            "source": "diagnostic",
            "data": {
                "message": "hello from pico",
            },
        },
    )
