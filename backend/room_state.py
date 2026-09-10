TEMERATURE_MIN = 19.0
TEMPERATURE_MAX = 25.0

HUMIDITY_MIN = 30.0
HUMIDITY_MAX = 60.0


def evaluate_room_state(temperature: float, humidity: float) -> list[str]:
    conditions = []

    if temperature < TEMERATURE_MIN:
        conditions.append("TOO_COLD")
    elif temperature > TEMPERATURE_MAX:
        conditions.append("TOO_HOT")

    if humidity < HUMIDITY_MIN:
        conditions.append("TOO_DRY")
    elif humidity > HUMIDITY_MAX:
        conditions.append("TOO_HUMID")

    if not conditions:
        conditions.append("HEALTHY")

    return conditions
