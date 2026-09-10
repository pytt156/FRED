RSSI_MIN = -70
LATENCY_MAX_MS = 150


def evaluate_network_state(
    connected: bool | None = None,
    rssi: int | None = None,
    latency_ms: int | None = None,
) -> list[str]:
    if connected is False:
        return ["OFFLINE"]

    network_degraded = (rssi is not None and rssi < RSSI_MIN) or (
        latency_ms is not None and latency_ms > LATENCY_MAX_MS
    )

    if network_degraded:
        return ["NETWORK_DEGRADED"]

    return []
