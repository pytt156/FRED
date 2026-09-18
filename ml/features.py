from ml.observation import RoomObservation


def observation_to_features(observation: RoomObservation) -> list[float]:
    observations = [
        observation.temperature,
        observation.humidity,
        observation.light,
        float(observation.motion),
        observation.rssi,
    ]

    return observations


def observations_to_features(observations: list[RoomObservation]) -> list[list[float]]:

    features = []

    for observation in observations:
        observation_features = observation_to_features(observation)
        features.append(observation_features)

    return features
