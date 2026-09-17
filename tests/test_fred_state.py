from fred_state import evaluate_fred_state, get_display_state


def test_healthy_room_makes_fred_happy():
    assert evaluate_fred_state(["HEALTHY"]) == ["HAPPY"]


def test_offline_room_disconnects_fred():
    assert evaluate_fred_state(["OFFLINE"]) == ["DISCONNECTED"]


def test_uncomfortable_room_makes_fred_uncomfortable():
    assert evaluate_fred_state(["TOO_HOT"]) == ["UNCOMFORTABLE"]


def test_multiple_conditions_create_multiple_fred_states():
    result = evaluate_fred_state(["TOO_DARK", "NETWORK_DEGRADED"])

    assert result == ["SLEEPY", "GRUMPY"]


def test_disconnected_has_highest_display_priority():
    result = get_display_state(["DISCONNECTED", "SLEEPY", "GRUMPY"])

    assert result == "DISCONNECTED"


def test_sleepy_has_priority_over_unhappy():
    result = get_display_state(["SLEEPY", "GRUMPY"])

    assert result == "SLEEPY"


def test_negative_states_show_unhappy():
    assert get_display_state(["GRUMPY"]) == "UNHAPPY"


def test_default_display_is_happy():
    assert get_display_state(["HAPPY"]) == "HAPPY"
