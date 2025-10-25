import pytest

from scripts.my_idea.flatten_func import flatten


@pytest.mark.parametrize(
    'data, expected',
    [
        (
            [1, [2, [3, [4, 5]]]],
            [1, 2, 3, 4, 5]
        ),
        (
            [1, [2, 3], {4, 5}],
            [1, 2, 3, 4, 5]
        ),
        (
            (1, 2, (3, (4, 5))),
            [1, 2, 3, 4, 5]
        ),
        (
            ['a', ['aa', 'foo', ['foo', 'bar']]],
            ['a', 'aa', 'foo', 'foo', 'bar']
        ),
    ]
)
def test_flatten(data, expected):
    result = flatten(data)
    assert expected == result, f'result must be {expected} not {result}'

