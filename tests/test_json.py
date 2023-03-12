import json
from typing import Optional
from src.json import get_diff


def test_get_diff_finds_differences_in_json_objects():
    sentinel = object()

    json_1 = json.dumps(
        {
            "a": "abc",
            "b": {
                "c": "def",
                "d": 123,
                "e": "xxx"
            }
        }
    )
    json_2 = json.dumps(
        {
            "a": "tuv",
            "b": {
                "c": "ghi",
                "d": 123
            }
        }
    )

    difference = get_diff(json_1, json_2, {}, sentinel)
    expected_difference = {
        "a": ("abc", "tuv"),
        "b": {
            "c": ("def", "ghi"),
            "e": ("xxx", sentinel)
        }
    }
    assert difference == expected_difference
