import pytest

from src.str_diff import get_diff


@pytest.mark.parametrize(
    "first_str, second_str, expected_diff",
    [
        ("SAMAT", "SAMSAMAN", [("", "SAM"), ("SAMA", "SAMA"), ("T", "N")]),
        (
            "Y1233345",
            "128845w",
            [("Y", ""), ("12", "12"), ("333", "88"), ("45", "45"), ("", "w")],
        ),
    ],
)
def test_get_diff_correctly_identifies_differences_in_strings(
    first_str, second_str, expected_diff
):
    difference = get_diff(first_str, second_str)
    assert difference == expected_diff
