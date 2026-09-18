from datetime import UTC, datetime

import pytest

from ml.anomaly_detector import AnomalyDetector
from ml.observation import RoomObservation
from ml.result import AnomalyResult
from ml.training_data import TRAINING_DATA


def test_anomaly_detector_fit():
    observations = [
        RoomObservation(
            timestamp=datetime(2026, 9, 18, 10, 0, tzinfo=UTC),
            temperature=22.0,
            humidity=45.0,
            light=50000.0,
            motion=True,
            rssi=-55.0,
        ),
        RoomObservation(
            timestamp=datetime(2026, 9, 18, 10, 1, tzinfo=UTC),
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


def test_anomaly_detector_predict_returns_result():
    observations = [
        RoomObservation(
            timestamp=datetime(2026, 9, 18, 10, i, tzinfo=UTC),
            temperature=22.0 + i * 0.1,
            humidity=45.0 + i * 0.2,
            light=50000.0 + i * 100,
            motion=True,
            rssi=-55.0 + i * 0.1,
        )
        for i in range(10)
    ]

    detector = AnomalyDetector()
    detector.fit(observations)

    observation = RoomObservation(
        timestamp=datetime(2026, 9, 18, 11, 0, tzinfo=UTC),
        temperature=22.3,
        humidity=45.5,
        light=50200.0,
        motion=True,
        rssi=-54.8,
    )

    result = detector.predict(observation)

    assert isinstance(result, AnomalyResult)
    assert isinstance(result.is_anomaly, bool)
    assert isinstance(result.score, float)


def test_anomaly_detector_ranks_unusual_observation_higher():
    training_data = TRAINING_DATA

    detector = AnomalyDetector()
    detector.fit(training_data)

    normal_observation = RoomObservation(
        datetime.now(tz=UTC), 22.0, 50.0, 50000, True, -55
    )
    unusual_observation = RoomObservation(
        datetime.now(tz=UTC), 29.0, 70.0, 15000, False, -85
    )

    normal_result = detector.predict(normal_observation)
    unusual_result = detector.predict(unusual_observation)

    assert unusual_result.score > normal_result.score
