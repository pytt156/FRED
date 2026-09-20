RSSI_MIN = -70


def evaluate_network_state(
    connected: bool | None = None,
    rssi: int | None = None,
) -> list[str]:
    if connected is None:
        return ["UNKNOWN"]

    if connected is False:
        return ["OFFLINE"]

    network_degraded = rssi is not None and rssi < RSSI_MIN

    if network_degraded:
        return ["NETWORK_DEGRADED"]

    return []
