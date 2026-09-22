from sklearn.ensemble import IsolationForest

from .features import observation_to_features, observations_to_features
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
        features = observation_to_features(observation)
        feature_matrix = [features]

        prediction = self.model.predict(feature_matrix)[0]
        raw_score = self.model.decision_function(feature_matrix)[0]

        is_anomaly = bool(prediction == -1)
        score = float(-raw_score)

        return AnomalyResult(is_anomaly=is_anomaly, score=score)
