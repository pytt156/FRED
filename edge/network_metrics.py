import network


wlan = network.WLAN(network.STA_IF)


def read_network_metrics():
    connected = wlan.isconnected()

    if connected:
        try:
            rssi = wlan.status("rssi")
        except Exception:
            rssi = None
    else:
        rssi = None

    network_data = {
        "connected": connected,
        "rssi": rssi
    }

    print(network_data)

    return network_data
