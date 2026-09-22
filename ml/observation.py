from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class RoomObservation:
    """A complete room telemetry observation available for ML processing."""

    timestamp: datetime
    temperature: float
    humidity: float
    light: float
    motion: bool
    rssi: float
