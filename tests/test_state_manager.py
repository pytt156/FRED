import importlib
import sys
from datetime import timedelta
from types import ModuleType
from typing import Any
from unittest.mock import Mock

import psycopg
import pytest
from requests import RequestException


class FakeLLMClient(ModuleType):
    generate_fred_response: Mock


fake_llm_client = FakeLLMClient("llm_client")
fake_llm_client.generate_fred_response = Mock()
sys.modules["llm_client"] = fake_llm_client

state_manager: Any = importlib.import_module("state_manager")


@pytest.fixture(autouse=True)
def reset_state_manager():
    state_manager.latest_room_data.update(
        {
            "temperature": None,
            "humidity": None,
            "light": None,
            "motion": None,
            "noise": None,
        }
    )

    state_manager.latest_room_seen.update(
        {
            "temperature": None,
            "humidity": None,
            "light": None,
        }
    )

    state_manager.latest_network_data.update(
        {
            "connected": None,
            "rssi": None,
        }
    )

    state_manager.last_room_state = None
    state_manager.last_fred_states = None
    state_manager.last_display_state = None


def mock_state_publication(monkeypatch):
    publish_room_state = Mock()

    monkeypatch.setattr(
        state_manager,
        "publish_room_state",
        publish_room_state,
    )
    monkeypatch.setattr(
        state_manager,
        "publish_fred_state",
        Mock(),
    )
    monkeypatch.setattr(
        state_manager,
        "should_react",
        Mock(return_value=False),
    )
    monkeypatch.setattr(
        state_manager,
        "evaluate_network_state",
        Mock(return_value=[]),
    )

    return publish_room_state


def set_fresh_required_signals():
    state_manager.latest_room_data.update(
        {
            "temperature": 22.0,
            "humidity": 45.0,
            "light": 40000,
        }
    )

    now = state_manager.datetime.now(state_manager.UTC)

    state_manager.latest_room_seen.update(
        {
            "temperature": now,
            "humidity": now,
            "light": now,
        }
    )

    return now


def test_db_failure_does_not_stop_state_publication(monkeypatch):
    client = Mock()

    monkeypatch.setattr(
        state_manager,
        "save_telemetry",
        Mock(side_effect=psycopg.Error("database unavailable")),
    )

    publish_room_state = Mock()
    publish_fred_state = Mock()

    monkeypatch.setattr(
        state_manager,
        "publish_room_state",
        publish_room_state,
    )
    monkeypatch.setattr(
        state_manager,
        "publish_fred_state",
        publish_fred_state,
    )
    monkeypatch.setattr(
        state_manager,
        "should_react",
        Mock(return_value=False),
    )

    data = {
        "source": "test",
        "data": {
            "connected": True,
            "rssi": -50,
        },
    }

    state_manager.handle_message(
        client,
        "fred/network/status",
        data,
    )

    publish_room_state.assert_called_once()
    publish_fred_state.assert_called_once()


def test_llm_failure_does_not_stop_state_publication(monkeypatch):
    client = Mock()

    publish_room_state = Mock()
    publish_fred_state = Mock()

    monkeypatch.setattr(
        state_manager,
        "save_telemetry",
        Mock(),
    )
    monkeypatch.setattr(
        state_manager,
        "publish_room_state",
        publish_room_state,
    )
    monkeypatch.setattr(
        state_manager,
        "publish_fred_state",
        publish_fred_state,
    )
    monkeypatch.setattr(
        state_manager,
        "should_react",
        Mock(return_value=True),
    )
    monkeypatch.setattr(
        state_manager,
        "generate_fred_response",
        Mock(side_effect=ValueError("LLM returned no text content")),
    )

    data = {
        "source": "test",
        "data": {
            "connected": True,
            "rssi": -50,
        },
    }

    state_manager.handle_message(
        client,
        "fred/network/status",
        data,
    )

    publish_room_state.assert_called_once()
    publish_fred_state.assert_called_once()


@pytest.mark.parametrize(
    "stale_signal",
    [
        "temperature",
        "humidity",
        "light",
    ],
)
def test_stale_required_signal_results_in_unknown_room_state(
    monkeypatch,
    stale_signal,
):
    client = Mock()
    publish_room_state = mock_state_publication(monkeypatch)

    now = set_fresh_required_signals()

    state_manager.latest_room_seen[stale_signal] = (
        now - state_manager.SENSOR_MAX_AGE - timedelta(seconds=1)
    )

    state_manager.handle_message(
        client,
        "fred/room/noise",
        {
            "source": "test",
            "data": {
                "noise": 30,
            },
        },
    )

    published_state = publish_room_state.call_args.args[1]

    assert published_state == ["UNKNOWN"]


def test_fresh_required_signals_keep_normal_room_state(monkeypatch):
    client = Mock()
    publish_room_state = mock_state_publication(monkeypatch)

    set_fresh_required_signals()

    state_manager.handle_message(
        client,
        "fred/room/noise",
        {
            "source": "test",
            "data": {
                "noise": 30,
            },
        },
    )

    published_state = publish_room_state.call_args.args[1]

    assert published_state == ["HEALTHY"]


def test_optional_signal_does_not_block_room_state(monkeypatch):
    client = Mock()
    publish_room_state = mock_state_publication(monkeypatch)

    set_fresh_required_signals()

    state_manager.latest_room_data["noise"] = None

    monkeypatch.setattr(
        state_manager,
        "update_motion",
        Mock(),
    )

    state_manager.handle_message(
        client,
        "fred/room/motion",
        {
            "source": "test",
            "data": {
                "motion": False,
            },
        },
    )

    published_state = publish_room_state.call_args.args[1]

    assert published_state == ["HEALTHY"]


def test_discord_failure_does_not_stop_tts(monkeypatch):
    client = Mock()

    set_fresh_required_signals()

    monkeypatch.setattr(
        state_manager,
        "should_react",
        Mock(return_value=True),
    )
    monkeypatch.setattr(
        state_manager,
        "generate_fred_response",
        Mock(return_value="Hello from FRED"),
    )
    monkeypatch.setattr(
        state_manager,
        "notify_discord",
        Mock(side_effect=RequestException("discord unavailable")),
    )

    generate_speech = Mock(return_value=(b"audio", 24000))
    publish_audio = Mock()

    monkeypatch.setattr(
        state_manager,
        "generate_speech",
        generate_speech,
    )
    monkeypatch.setattr(
        state_manager,
        "publish_audio",
        publish_audio,
    )

    state_manager.handle_message(
        client,
        "fred/room/noise",
        {
            "source": "test",
            "data": {
                "noise": 30,
            },
        },
    )

    generate_speech.assert_called_once_with("Hello from FRED")
    publish_audio.assert_called_once_with(
        client,
        b"audio",
        24000,
    )


def test_tts_failure_does_not_escape_handle_message(monkeypatch):
    client = Mock()

    set_fresh_required_signals()

    monkeypatch.setattr(
        state_manager,
        "should_react",
        Mock(return_value=True),
    )
    monkeypatch.setattr(
        state_manager,
        "generate_fred_response",
        Mock(return_value="Hello from FRED"),
    )
    monkeypatch.setattr(
        state_manager,
        "notify_discord",
        Mock(),
    )
    monkeypatch.setattr(
        state_manager,
        "generate_speech",
        Mock(side_effect=RuntimeError("tts unavailable")),
    )

    publish_audio = Mock()

    monkeypatch.setattr(
        state_manager,
        "publish_audio",
        publish_audio,
    )

    state_manager.handle_message(
        client,
        "fred/room/noise",
        {
            "source": "test",
            "data": {
                "noise": 30,
            },
        },
    )

    publish_audio.assert_not_called()
