from ..user_based_CF import collaborative_filtering


def test_input(input_data):
    assert type(input_data) is dict
    assert len(input_data) > 0


def test_euclidean_distance(input_data):
    obj = collaborative_filtering.CF(input_data, distance_method="euclidean_distance")
    res = obj.euclidean_distance(1, 2)
    assert type(res) is float
    assert res > 0


def test_manhattan_distance(input_data):
    obj = collaborative_filtering.CF(input_data, distance_method="manhattan_distance")
    res = obj.manhattan_distance(1, 2)
    assert type(res) is float
    assert res > 0


def test_RC(input_data):
    obj = collaborative_filtering.CF(input_data, distance_method="euclidean_distance")
    res = obj.recommendation_res(1)
    assert type(res) is list
