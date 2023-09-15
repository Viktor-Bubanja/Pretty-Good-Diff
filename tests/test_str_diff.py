import pytest

from src.str_diff import get_diff


@pytest.mark.parametrize(
    "first_str, second_str, expected_diff",
    [
        (
            "some really l",
            "some really really l",
            [
                (0, 0),
                (1, 1),
                (2, 2),
                (3, 3),
                (4, 4),
                (5, 5),
                (6, 6),
                (7, 7),
                (8, 8),
                (9, 9),
                (10, 10),
                (11, 11),
                (12, 15),
            ],
        ),
        ("ABCDE", "BCABC", [(0, 2), (1, 3), (2, 4)]),
        (
            "DESC A LIT DIFF",
            "DESC DIFF",
            [
                (0, 0),
                (1, 1),
                (2, 2),
                (3, 3),
                (10, 4),
                (11, 5),
                (12, 6),
                (13, 7),
                (14, 8),
            ],
        ),
        ("SAMAT", "SAMSAMAN", [(0, 3), (1, 4), (2, 5), (3, 6)]),
        ("Y1233345", "128845w", [(1, 0), (2, 1), (6, 4), (7, 5)]),
        ("xxx", "yyy", []),
    ],
)
def test_get_dynamic_programming_diff_correctly_identifies_differences_in_strings(
    first_str, second_str, expected_diff
):
    difference = get_diff(first_str, second_str)
    assert difference == expected_diff
