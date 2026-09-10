TEMERATURE_MIN = 19.0
TEMPERATURE_MAX = 25.0

HUMIDITY_MIN = 30.0
HUMIDITY_MAX = 60.0

LIGHT_MIN = 30000  # temporary until we have calibrated with physical sensors

NOISE_MAX = 70  # simulated normalized interval: 0-100


def evaluate_room_state(
    temperature: float | None = None,
    humidity: float | None = None,
    light: float | None = None,
    noise: float | None = None,
) -> list[str]:
    conditions = []

    if temperature is not None:
        if temperature < TEMERATURE_MIN:
            conditions.append("TOO_COLD")
        elif temperature > TEMPERATURE_MAX:
            conditions.append("TOO_HOT")

    if humidity is not None:
        if humidity < HUMIDITY_MIN:
            conditions.append("TOO_DRY")
        elif humidity > HUMIDITY_MAX:
            conditions.append("TOO_HUMID")

    if light is not None and light < LIGHT_MIN:
        conditions.append("TOO_DARK")

    if noise is not None and noise > NOISE_MAX:
        conditions.append("TOO_NOISY")

    if not conditions:
        conditions.append("HEALTHY")

    return conditions
