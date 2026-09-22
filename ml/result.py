from dataclasses import dataclass


@dataclass(frozen=True)
class AnomalyResult:
    """Result of anomaly detection for a room observation."""

    is_anomaly: bool
    score: float
