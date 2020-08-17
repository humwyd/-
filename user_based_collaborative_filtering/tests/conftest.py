import pytest


@pytest.fixture(scope="module")
def input_data():
    input_data = {1: {'Python let you know': 2.5, 'snakes on a plane': 3.5, 'just my luck': 3.0, 'superman returns': 3.5,
                      'you,me and dupree': 2.5, 'the night listener': 3.0},
                  2: {'Python let you know': 3.0, 'snakes on a plane': 3.5, 'just my luck': 1.5, 'superman returns': 5.0,
                      'you,me and dupree': 3.5, 'the night listener': 3.0},
                  3: {'Python let you know': 2.5, 'snakes on a plane': 3.0, 'superman returns': 3.5,
                      'the night listener': 4.0},
                  4: {'snakes on a plane': 3.5, 'just my luck': 3.0, 'superman returns': 4.0,
                      'the night listener': 4.5},
                  5: {'Python let you know': 3.0, 'snakes on a plane': 4.0, 'just my luck': 2.0, 'superman returns': 3.0,
                      'you,me and dupree': 2.0, 'the night listener': 3.0},
                  6: {'Python let you know': 3.0, 'snakes on a plane': 4.0, 'superman returns': 5.0, 'you,me and dupree': 3.5,
                      'the night listener': 3.0},
                  7: {'snakes on a plane': 4.5, 'superman returns': 4.0, 'you,me and dupree': 1.0},
                  8: {'abc': 1.2}}

    return input_data
