import importlib
import sys
from types import ModuleType
from unittest.mock import Mock


def test_invalid_json_is_ignored(monkeypatch):
    fake_state_manager = ModuleType("state_manager")
    fake_handle_message = Mock()
    fake_state_manager.handle_message = fake_handle_message

    monkeypatch.setitem(sys.modules, "state_manager", fake_state_manager)
    sys.modules.pop("consumer", None)

    consumer = importlib.import_module("consumer")

    message = Mock()
    message.payload = b"{not valid json"
    message.topic = "fred/room/metrics"

    consumer.on_message(Mock(), None, message)

    fake_handle_message.assert_not_called()


def test_payload_without_data_is_ignored(monkeypatch):
    fake_state_manager = ModuleType("state_manager")
    fake_handle_message = Mock()
    fake_state_manager.handle_message = fake_handle_message

    monkeypatch.setitem(sys.modules, "state_manager", fake_state_manager)
    sys.modules.pop("consumer", None)

    consumer = importlib.import_module("consumer")

    message = Mock()
    message.payload = b'{"source": "test"}'
    message.topic = "fred/room/metrics"

    consumer.on_message(Mock(), None, message)

    fake_handle_message.assert_not_called()
