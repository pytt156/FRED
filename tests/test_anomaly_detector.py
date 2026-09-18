import datetime

import pytest

from ml.anomaly_detector import AnomalyDetector
from ml.observation import RoomObservation


def test_anomaly_detector_fit():
    observations = [
        RoomObservation(
            timestamp=datetime.datetime(2026, 9, 18, 10, 0, tzinfo=datetime.UTC),
            temperature=22.0,
            humidity=45.0,
            light=50000.0,
            motion=True,
            rssi=-55.0,
        ),
        RoomObservation(
            timestamp=datetime.datetime(2026, 9, 18, 10, 1, tzinfo=datetime.UTC),
            temperature=22.2,
            humidity=46.0,
            light=49000.0,
            motion=False,
            rssi=-54.0,
        ),
    ]

    detector = AnomalyDetector()

    detector.fit(observations)

    assert hasattr(detector.model, "estimators_")


def test_anomaly_detector_fit_requires_observations():
    observations = []
    detector = AnomalyDetector()

    with pytest.raises(ValueError):
        detector.fit(observations)
