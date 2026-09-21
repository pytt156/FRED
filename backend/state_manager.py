from datetime import UTC, datetime, timedelta

import psycopg
from audio_publisher import publish_audio
from discord_notifier import send_discord_message
from fred_state import evaluate_fred_state, get_display_state
from interaction import should_react
from llm_client import generate_fred_response
from network_state import evaluate_network_state
from openai import APIError
from persistence import save_telemetry
from presence import is_presence_active, update_motion
from publisher import publish_fred_state, publish_room_state
from requests import RequestException
from room_state import evaluate_room_state
from tts_client import generate_speech

SENSOR_MAX_AGE = timedelta(seconds=60)

latest_room_seen: dict[str, datetime | None] = {
    "temperature": None,
    "humidity": None,
    "light": None,
}

latest_room_data = {
    "temperature": None,
    "humidity": None,
    "light": None,
    "motion": None,
    "noise": None,
}

latest_network_data = {
    "connected": None,
    "rssi": None,
}

last_room_state = None
last_fred_states = None
last_display_state = None


def notify_discord(
    fred_response: str,
    room_state: list[str],
) -> None:
    abnormal_states = [
        state for state in room_state if state not in {"HEALTHY", "UNKNOWN"}
    ]

    discord_message = fred_response

    if abnormal_states:
        discord_message += f"\n\nStates: {', '.join(abnormal_states)}"

    send_discord_message(discord_message)


def handle_message(client, topic, data):
    global last_room_state, last_fred_states, last_display_state

    if topic == "fred/interaction/button":
        room_state = last_room_state or ["UNKNOWN"]

        try:
            fred_response = generate_fred_response(
                room_state=room_state,
                fred_state=last_fred_states or [],
                display_state=last_display_state or "UNKNOWN",
                presence_active=True,
                trigger="button",
            )
        except (APIError, ValueError) as exc:
            print(f"LLM response failed: {exc}")
            return

        print(f"FRED says: {fred_response}")

        try:
            notify_discord(
                fred_response=fred_response,
                room_state=room_state,
            )
        except RequestException as exc:
            print(f"Discord notification failed: {exc}")

        try:
            audio_bytes, sample_rate = generate_speech(fred_response)
        except (APIError, FileNotFoundError, RuntimeError) as exc:
            print(f"TTS failed: {exc}")
            return

        publish_audio(
            client,
            audio_bytes,
            sample_rate,
        )

        return

    if topic == "fred/room/metrics":
        latest_room_data["temperature"] = data["data"].get("temperature")
        latest_room_data["humidity"] = data["data"].get("humidity")

        now = datetime.now(UTC)
        latest_room_seen["temperature"] = now
        latest_room_seen["humidity"] = now

    elif topic == "fred/room/light":
        latest_room_data["light"] = data["data"].get("light")
        latest_room_seen["light"] = datetime.now(UTC)

    elif topic == "fred/room/noise":
        latest_room_data["noise"] = data["data"].get("noise")

    elif topic == "fred/room/motion":
        motion = data["data"].get("motion")
        latest_room_data["motion"] = motion
        update_motion(motion)

    elif topic == "fred/network/status":
        latest_network_data["connected"] = data["data"].get("connected")
        latest_network_data["rssi"] = data["data"].get("rssi")

        try:
            save_telemetry(
                time=datetime.now(UTC),
                device_id="fred-pico-01",
                source=data.get("source", "real"),
                temperature=latest_room_data["temperature"],
                humidity=latest_room_data["humidity"],
                light=latest_room_data["light"],
                motion=latest_room_data["motion"],
                wifi_connected=latest_network_data["connected"],
                rssi=latest_network_data["rssi"],
            )
        except psycopg.Error as exc:
            print(f"Failed to save telemetry: {exc}")

    now = datetime.now(UTC)

    temperature = (
        latest_room_data["temperature"]
        if latest_room_seen["temperature"] is not None
        and now - latest_room_seen["temperature"] <= SENSOR_MAX_AGE
        else None
    )

    humidity = (
        latest_room_data["humidity"]
        if latest_room_seen["humidity"] is not None
        and now - latest_room_seen["humidity"] <= SENSOR_MAX_AGE
        else None
    )

    light = (
        latest_room_data["light"]
        if latest_room_seen["light"] is not None
        and now - latest_room_seen["light"] <= SENSOR_MAX_AGE
        else None
    )

    room_conditions = evaluate_room_state(
        temperature=temperature,
        humidity=humidity,
        light=light,
        noise=latest_room_data["noise"],
    )

    network_conditions = evaluate_network_state(
        connected=latest_network_data["connected"],
        rssi=latest_network_data["rssi"],
    )

    if "OFFLINE" in network_conditions:
        room_state = ["OFFLINE"]
    else:
        room_state = room_conditions + network_conditions

    fred_states = evaluate_fred_state(room_state)
    display_state = get_display_state(fred_states)

    fred_changed = fred_states != last_fred_states
    display_changed = display_state != last_display_state

    presence_active = is_presence_active()

    # Publish deterministic state before optional external side effects.
    if room_state != last_room_state:
        print(f"room state changed: {room_state}")
        publish_room_state(client, room_state)
        last_room_state = room_state

    if fred_changed or display_changed:
        print(f"fred state changed: {fred_states}, display state: {display_state}")

        publish_fred_state(
            client,
            fred_states,
            display_state,
        )

        last_fred_states = fred_states
        last_display_state = display_state

    react = should_react(
        presence_active=presence_active,
        state_changed=fred_changed,
        fred_states=fred_states,
    )

    if not react:
        return

    try:
        fred_response = generate_fred_response(
            room_state=room_state,
            fred_state=fred_states,
            display_state=display_state,
            presence_active=presence_active,
            trigger="spontaneous",
        )
    except (APIError, ValueError) as exc:
        print(f"LLM response failed: {exc}")
        return

    print(f"FRED says: {fred_response}")

    try:
        notify_discord(
            fred_response=fred_response,
            room_state=room_state,
        )
    except RequestException as exc:
        print(f"Discord notification failed: {exc}")

    try:
        audio_bytes, sample_rate = generate_speech(fred_response)
    except (APIError, FileNotFoundError, RuntimeError) as exc:
        print(f"TTS failed: {exc}")
        return

    publish_audio(
        client,
        audio_bytes,
        sample_rate,
    )
