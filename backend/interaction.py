def should_react(
    presence_active: bool,
    state_changed: bool,
) -> bool:
    return presence_active and state_changed
