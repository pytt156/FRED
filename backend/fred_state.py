def evaluate_fred_state(room_conditions: list[str]) -> list[str]:
    if "OFFLINE" in room_conditions:
        return ["DISCONNECTED"]

    states = []

    if any(
        condition in room_conditions
        for condition in ("TOO_HOT", "TOO_COLD", "TOO_DRY", "TOO_HUMID")
    ):
        states.append("UNCOMFORTABLE")
    if "TOO_NOISY" in room_conditions:
        states.append("OVERSTIMULATED")
    if "TOO_DARK" in room_conditions:
        states.append("SLEEPY")
    if "NETWORK_DEGRADED" in room_conditions:
        states.append("GRUMPY")
    if room_conditions == ["HEALTHY"]:
        states.append("HAPPY")

    return states


def get_display_state(fred_states: list[str]) -> str:
    if "DISCONNECTED" in fred_states:
        return "DISCONNECTED"

    if "SLEEPY" in fred_states:
        return "SLEEPY"

    if any(
        state in fred_states for state in ("GRUMPY", "UNCOMFORTABLE", "OVERSTIMULATED")
    ):
        return "UNHAPPY"

    return "HAPPY"
