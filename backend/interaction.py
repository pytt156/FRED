def should_react(
    presence_active: bool, state_changed: bool, fred_states: list[str]
) -> bool:
    if "DISCONNECTED" in fred_states:
        return False

    return presence_active and state_changed
