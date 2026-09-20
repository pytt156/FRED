from room_state import evaluate_room_state


def room_with(**overrides):
    data = {
        "temperature": 22.0,
        "humidity": 45.0,
        "light": 40000,
        "noise": None,
    }
    data.update(overrides)
    return data


def test_healthy_room():
    assert evaluate_room_state(**room_with()) == ["HEALTHY"]


def test_temperature_too_cold():
    assert evaluate_room_state(**room_with(temperature=18.0)) == ["TOO_COLD"]


def test_temperature_too_hot():
    assert evaluate_room_state(**room_with(temperature=26.0)) == ["TOO_HOT"]


def test_humidity_too_dry():
    assert evaluate_room_state(**room_with(humidity=29.0)) == ["TOO_DRY"]


def test_humidity_too_humid():
    assert evaluate_room_state(**room_with(humidity=61.0)) == ["TOO_HUMID"]


def test_room_too_dark():
    assert evaluate_room_state(**room_with(light=29999)) == ["TOO_DARK"]


def test_room_too_noisy():
    assert evaluate_room_state(**room_with(noise=71)) == ["TOO_NOISY"]


def test_multiple_bad_conditions():
    assert evaluate_room_state(
        **room_with(
            temperature=26.0,
            humidity=29.0,
            light=29999,
            noise=71,
        )
    ) == [
        "TOO_HOT",
        "TOO_DRY",
        "TOO_DARK",
        "TOO_NOISY",
    ]


def test_boundary_values_are_healthy():
    assert evaluate_room_state(
        temperature=19.0,
        humidity=30.0,
        light=30000,
        noise=70,
    ) == ["HEALTHY"]

    assert evaluate_room_state(
        temperature=25.0,
        humidity=60.0,
        light=30000,
        noise=70,
    ) == ["HEALTHY"]


def test_missing_temperature_is_unknown():
    assert evaluate_room_state(
        temperature=None,
        humidity=45.0,
        light=40000,
    ) == ["UNKNOWN"]


def test_missing_humidity_is_unknown():
    assert evaluate_room_state(
        temperature=22.0,
        humidity=None,
        light=40000,
    ) == ["UNKNOWN"]


def test_missing_light_is_unknown():
    assert evaluate_room_state(
        temperature=22.0,
        humidity=45.0,
        light=None,
    ) == ["UNKNOWN"]
