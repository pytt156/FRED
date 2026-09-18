from datetime import UTC, datetime

from .observation import RoomObservation

TRAINING_DATA = [
    RoomObservation(datetime.now(UTC), 22.0, 46.0, 52025.0, True, -44.0),
    RoomObservation(datetime.now(UTC), 21.0, 45.0, 52010.0, True, -65.0),
    RoomObservation(datetime.now(UTC), 23.0, 55.0, 42032.0, False, -56.0),
    RoomObservation(datetime.now(UTC), 23.0, 53.0, 56030.0, False, -45.0),
    RoomObservation(datetime.now(UTC), 24.0, 42.0, 43260.0, False, -68.0),
    RoomObservation(datetime.now(UTC), 22.0, 43.0, 55000.0, True, -56.0),
    RoomObservation(datetime.now(UTC), 24.0, 52.0, 44236.0, True, -41.0),
]
