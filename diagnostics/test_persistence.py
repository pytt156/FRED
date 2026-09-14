from datetime import datetime, timezone

from persistence import save_telemetry


save_telemetry(
    time=datetime.now(timezone.utc),
    device_id="fred-pico-01",
    source="test",
    temperature=22.5,
    humidity=53.0,
    light=47000,
    motion=True,
    wifi_connected=True,
    rssi=-33
)