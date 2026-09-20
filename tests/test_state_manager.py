import importlib
import sys
from types import ModuleType
from typing import Any
from unittest.mock import Mock

import psycopg
import pytest


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

    state_manager.latest_network_data.update(
        {
            "connected": None,
            "rssi": None,
        }
    )

    state_manager.last_room_state = None
    state_manager.last_fred_states = None
    state_manager.last_display_state = None


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
