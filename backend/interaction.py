import time

SPONTANEOUS_COOLDOWN_SECONDS = 60

last_spontaneous_reaction_at = None


def should_react(
    presence_active: bool,
    state_changed: bool,
    fred_states: list[str],
    trigger: str = "spontaneous",
) -> bool:
    global last_spontaneous_reaction_at

    if trigger == "button":
        return True

    if "DISCONNECTED" in fred_states:
        return False

    if not presence_active or not state_changed:
        return False

    now = time.time()

    if (
        last_spontaneous_reaction_at is not None
        and now - last_spontaneous_reaction_at < SPONTANEOUS_COOLDOWN_SECONDS
    ):
        return False

    last_spontaneous_reaction_at = now
    return True
