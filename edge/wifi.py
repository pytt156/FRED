import json
import network
import rp2
import time


rp2.country("SE")

with open("wifi_credentials.json") as file:
    credentials = json.load(file)


def connect_wifi(waiting_time=10):
    # station interface -> makes into client mode
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)  # powers on radio WIFI on pico
    wlan.connect(credentials.get("wifi_ssid"), credentials.get("wifi_password"))
    print(wlan)

    # (device ip, subnet mask, router/gateway, DNS server)
    print(f"{wlan.ifconfig()}")

    while waiting_time > 0:
        if wlan.isconnected():
            print("Connected to wifi")
            break

        waiting_time -= 1
        print("Trying to connect wifi, pls wait")
        time.sleep(2)

    return wlan.isconnected()