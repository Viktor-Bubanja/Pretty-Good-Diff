import json
from typing import Optional

import pytest
from pydantic import BaseModel

from src.diff import get_diff
from src.sentinel import sentinel


def test_get_diff_finds_differences_in_json_objects():
    json_1 = json.dumps({"a": "abc", "b": {"c": "aaa", "d": 123, "e": "xxx"}})
    json_2 = json.dumps({"a": "tuv", "b": {"c": "bab", "d": 123}})

    difference = get_diff(json_1, json_2)
    expected_difference = {
        "a": [],
        "b": {"c": [(0, 1)], "e": ("xxx", sentinel)},
    }
    assert difference == expected_difference


def test_get_diff_finds_differences_in_nested_pydantic_objects_converted_to_dicts():
    class SomeNestedClass(BaseModel):
        c: str
        d: int
        e: Optional[str]

    class SomeClass(BaseModel):
        a: str
        b: SomeNestedClass

    obj_1 = SomeClass(a="abc", b=SomeNestedClass(c="xyz", d=123, e="xxx"))
    obj_2 = SomeClass(a="tuv", b=SomeNestedClass(c="yza", d=123))

    difference = get_diff(obj_1.dict(), obj_2.dict())
    expected_difference = {
        "a": [],
        "b": {"c": [(1, 0), (2, 1)], "e": ("xxx", None)},
    }
    assert difference == expected_difference


@pytest.mark.parametrize(
    "first_object, second_object, expected_diff",
    [
        (
            {
                "a": 123,
                "b": {
                    "c": "zzz",
                    "d": "xxx",
                    "e": {"f": None, "g": 6, "h": 5, "i": "ababc"},
                },
                "i": 456,
                "j": 1,
            },
            {
                "a": 123,
                "b": {"c": "zzz", "d": "yyy", "e": {"f": 4, "g": 6, "i": "abcde"}},
                "i": 789,
                "k": 2,
            },
            {
                "b": {
                    "d": [],
                    "e": {
                        "f": (None, 4),
                        "h": (5, sentinel),
                        "i": [(2, 0), (3, 1), (4, 2)],
                    },
                },
                "i": (456, 789),
                "j": (1, sentinel),
                "k": (sentinel, 2),
            },
        ),
        (
            {
                "id": "12345",
                "location": {
                    "street_name": "Totally real street name",
                    "street_number": "27",
                },
                "description": {
                    "en": None,
                    "de": "Some really long description that is diff",
                },
            },
            {
                "id": "12845",
                "location": {
                    "street_name": "Totally real street name st",
                    "street_number": "27",
                },
                "description": {
                    "en": None,
                    "de": "A really really long description that is different",
                },
            },
            {
                "description": {
                    "de": [
                        (3, 3),
                        (4, 8),
                        (5, 9),
                        (6, 10),
                        (7, 11),
                        (8, 12),
                        (9, 13),
                        (10, 14),
                        (11, 15),
                        (12, 16),
                        (13, 17),
                        (14, 18),
                        (15, 19),
                        (16, 20),
                        (17, 21),
                        (18, 22),
                        (19, 23),
                        (20, 24),
                        (21, 25),
                        (22, 26),
                        (23, 27),
                        (24, 28),
                        (25, 29),
                        (26, 30),
                        (27, 31),
                        (28, 32),
                        (29, 33),
                        (30, 34),
                        (31, 35),
                        (32, 36),
                        (33, 37),
                        (34, 38),
                        (35, 39),
                        (36, 40),
                        (37, 41),
                        (38, 42),
                        (39, 43),
                        (40, 44),
                    ]
                },
                "location": {
                    "street_name": [
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
                        (12, 12),
                        (13, 13),
                        (14, 14),
                        (15, 15),
                        (16, 16),
                        (17, 17),
                        (18, 18),
                        (19, 19),
                        (20, 20),
                        (21, 21),
                        (22, 22),
                        (23, 23),
                    ]
                },
                "id": [(0, 0), (1, 1), (3, 3), (4, 4)],
            },
        ),
    ],
)
def test_get_diff_finds_differences_in_nested_dictionaries(
    first_object, second_object, expected_diff
):
    difference = get_diff(first_object, second_object)
    assert difference == expected_diff
