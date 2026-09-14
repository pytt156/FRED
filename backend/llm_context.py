from prompts import SYSTEM_PROMPT


def build_state_context(
    room_state: list[str],
    fred_state: list[str],
    display_state: str,
    presence_active: bool,
    trigger: str,
) -> str:
    return f"""
<current_state>
room_state: {room_state}
fred_state: {fred_state}
display_state: {display_state}
presence_active: {presence_active}
<current_state>

<event>
type: {trigger}
</event>
""".strip()


def build_llm_input(
    room_state: list[str],
    fred_state: list[str],
    display_state: str,
    presence_active: bool,
    trigger: str,
) -> str:
    state_context = build_state_context(
        room_state=room_state,
        fred_state=fred_state,
        display_state=display_state,
        presence_active=presence_active,
        trigger=trigger,
    )

    return f"{SYSTEM_PROMPT}\n\n{state_context}"
