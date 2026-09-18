from room_state import evaluate_room_state


def test_healthy_room():
    result = evaluate_room_state(
        temperature=22.0,
        humidity=45.0,
        light=50000,
        noise=30,
    )

    assert result == ["HEALTHY"]


def test_temperature_too_cold():
    assert evaluate_room_state(temperature=18.0) == ["TOO_COLD"]


def test_temperature_too_hot():
    assert evaluate_room_state(temperature=26.0) == ["TOO_HOT"]


def test_humidity_too_dry():
    assert evaluate_room_state(humidity=29.0) == ["TOO_DRY"]


def test_humidity_too_humid():
    assert evaluate_room_state(humidity=61.0) == ["TOO_HUMID"]


def test_room_too_dark():
    assert evaluate_room_state(light=29999) == ["TOO_DARK"]


def test_room_too_noisy():
    assert evaluate_room_state(noise=71) == ["TOO_NOISY"]


def test_multiple_bad_conditions():
    result = evaluate_room_state(
        temperature=27.0,
        humidity=20.0,
        light=10000,
        noise=90,
    )

    assert result == [
        "TOO_HOT",
        "TOO_DRY",
        "TOO_DARK",
        "TOO_NOISY",
    ]


def test_boundary_values_are_healthy():
    result = evaluate_room_state(
        temperature=19.0,
        humidity=30.0,
        light=30000,
        noise=70,
    )

    assert result == ["HEALTHY"]
