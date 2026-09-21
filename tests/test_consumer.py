import importlib
import sys
from types import ModuleType
from unittest.mock import Mock


class FakeStateManager(ModuleType):
    handle_message: Mock


def load_consumer(monkeypatch):
    fake_state_manager = FakeStateManager("state_manager")
    fake_state_manager.handle_message = Mock()

    monkeypatch.setitem(
        sys.modules,
        "state_manager",
        fake_state_manager,
    )
    sys.modules.pop("consumer", None)

    consumer = importlib.import_module("consumer")

    return consumer, fake_state_manager.handle_message


def test_invalid_json_is_ignored(monkeypatch):
    consumer, handle_message = load_consumer(monkeypatch)

    message = Mock()
    message.payload = b"{not valid json"
    message.topic = "fred/room/metrics"

    consumer.on_message(
        Mock(),
        None,
        message,
    )

    handle_message.assert_not_called()


def test_payload_without_data_is_ignored(monkeypatch):
    consumer, handle_message = load_consumer(monkeypatch)

    message = Mock()
    message.payload = b'{"source": "test"}'
    message.topic = "fred/room/metrics"

    consumer.on_message(
        Mock(),
        None,
        message,
    )

    handle_message.assert_not_called()
