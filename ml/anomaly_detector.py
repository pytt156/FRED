from sklearn.ensemble import IsolationForest

from .features import observations_to_features
from .observation import RoomObservation
from .result import AnomalyResult


class AnomalyDetector:
    def __init__(self):
        self.model = IsolationForest(random_state=42)

    def fit(self, observations: list[RoomObservation]) -> None:
        if not observations:
            raise ValueError("Cannot train anomaly detector without observations.")

        features = observations_to_features(observations)
        self.model.fit(features)

    def predict(self, observation: RoomObservation) -> AnomalyResult:
        raise NotImplementedError
