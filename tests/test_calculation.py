def test_emissions():
    count = 100
    distance = 10
    factor = 0.18

    result = count * distance * factor

    assert result == 180
