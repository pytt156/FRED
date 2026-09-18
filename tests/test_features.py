import datetime

from ml.features import observation_to_features, observations_to_features
from ml.observation import RoomObservation


def test_observation_to_features():

    observation = RoomObservation(
        timestamp=datetime.datetime(2006, 9, 18, 10, 0, tzinfo=datetime.UTC),
        temperature=22.5,
        humidity=45.0,
        light=50000.0,
        motion=True,
        rssi=-55.0,
    )

    features = observation_to_features(observation)

    assert features == [22.5, 45.0, 50000.0, 1.0, -55.0]


def test_observations_to_features():

    features = observations_to_features(
        [
            RoomObservation(
                timestamp=datetime.datetime(2006, 9, 18, 10, 0, tzinfo=datetime.UTC),
                temperature=22.5,
                humidity=45.0,
                light=50000.0,
                motion=True,
                rssi=-55.0,
            ),
            RoomObservation(
                timestamp=datetime.datetime(2026, 7, 18, 11, 3, tzinfo=datetime.UTC),
                temperature=20.5,
                humidity=55.0,
                light=55000.0,
                motion=True,
                rssi=-65.0,
            ),
        ]
    )

    assert features == [
        [22.5, 45, 50000.0, 1.0, -55.0],
        [20.5, 55.0, 55000.0, 1.0, -65.0],
    ]
