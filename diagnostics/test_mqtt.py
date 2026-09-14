from wifi import connect_wifi
from mqtt_client import connect_mqtt, publish_message

import time


if connect_wifi():

    if connect_mqtt():

        publish_message(
            b"fred/test",
            b"hello from pico"
        )