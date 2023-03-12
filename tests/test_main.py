import json
from typing import Optional
from src.main import get_diff
from pydantic import BaseModel


def test_get_diff_finds_differences_in_nested_dictionaries():
    sentinel = object()
    dictionary_1 = {"a": 123, "b": {"c": "zzz", "d": "xxx", "e": {"f": None, "g": 6, "h": 5}}, "i": 456, "j": 1}
    dictionary_2 = {"a": 123, "b": {"c": "zzz", "d": "yyy", "e": {"f": 4, "g": 6}}, "i": 789, "k": 2}

    difference = get_diff(dictionary_1, dictionary_2, sentinel)
    expected_difference = {
        "b": {
            "d": ("xxx", "yyy"),
            "e": {
                "f": (None, 4),
                "h": (5, sentinel),
            },
        },
        "i": (456, 789),
        "j": (1, sentinel),
        "k": (sentinel, 2),
    }
    assert difference == expected_difference


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

    difference = get_diff(json_1, json_2, sentinel)
    expected_difference = {
        "a": ("abc", "tuv"),
        "b": {
            "c": ("def", "ghi"),
            "e": ("xxx", sentinel)
        }
    }
    assert difference == expected_difference

def test_get_diff_finds_differences_in_nested_pydantic_objects():
    sentinel = object()
    class SomeNestedClass(BaseModel):
        c: str
        d: int
        e: Optional[str]

    class SomeClass(BaseModel):
        a: str
        b: SomeNestedClass
    obj_1 = SomeClass(a="abc", b=SomeNestedClass(c="def", d=123, e="xxx"))
    obj_2 = SomeClass(a="tuv", b=SomeNestedClass(c="ghi", d=123))

    difference = get_diff(obj_1, obj_2, sentinel)
    expected_difference = {
        "a": ("abc", "tuv"),
        "b": {
            "c": ("def", "ghi"),
            "e": ("xxx", None)
        }
    }
    assert difference == expected_difference
