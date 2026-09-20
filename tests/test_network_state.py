from network_state import evaluate_network_state


def test_offline_network():
    result = evaluate_network_state(
        connected=False,
        rssi=-50,
    )

    assert result == ["OFFLINE"]


def test_degraded_network():
    result = evaluate_network_state(
        connected=True,
        rssi=-71,
    )

    assert result == ["NETWORK_DEGRADED"]


def test_healthy_network():
    result = evaluate_network_state(
        connected=True,
        rssi=-55,
    )

    assert result == []


def test_rssi_boundary_is_not_degraded():
    result = evaluate_network_state(
        connected=True,
        rssi=-70,
    )

    assert result == []


def test_missing_rssi_is_not_degraded():
    result = evaluate_network_state(
        connected=True,
        rssi=None,
    )

    assert result == []


def test_missing_connection_state_is_unknown():
    assert evaluate_network_state(
        connected=None,
        rssi=None,
    ) == ["UNKNOWN"]
