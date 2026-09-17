import json
import network
import ntptime
import rp2
import time


rp2.country("SE")

with open("wifi_credentials.json") as file:
    credentials = json.load(file)


def sync_time():
    try:
        print("Synchronizing time with NTP...")
        ntptime.settime()
        print("NTP time synchronized")
        print("Current UTC time:", time.localtime())
        return True

    except Exception as error:
        print("NTP time sync failed:", error)
        return False


def connect_wifi(waiting_time=10):
    # Station interface -> client mode
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(
        credentials.get("wifi_ssid"),
        credentials.get("wifi_password"),
    )

    print(wlan)
    print(wlan.ifconfig())

    while waiting_time > 0:
        print("WiFi status:", wlan.status())

        if wlan.isconnected():
            print("Connected to wifi")
            print("Network config:", wlan.ifconfig())

            # TLS certificate validation requires a correct clock.
            if not sync_time():
                print("WARNING: Time synchronization failed")

            return True

        waiting_time -= 1
        print("Trying to connect wifi, pls wait")
        time.sleep(2)

    print("WiFi connection failed")
    return False