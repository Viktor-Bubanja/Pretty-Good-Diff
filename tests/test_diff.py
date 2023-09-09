import json
from typing import Optional

from pydantic import BaseModel

from src.diff import get_diff, show_diff
from src.sentinel import sentinel


def test_get_diff_finds_differences_in_nested_dictionaries():
    dictionary_1 = {
        "a": 123,
        "b": {"c": "zzz", "d": "xxx", "e": {"f": None, "g": 6, "h": 5}},
        "i": 456,
        "j": 1,
    }
    dictionary_2 = {
        "a": 123,
        "b": {"c": "zzz", "d": "yyy", "e": {"f": 4, "g": 6}},
        "i": 789,
        "k": 2,
    }

    difference = get_diff(dictionary_1, dictionary_2)
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
    json_1 = json.dumps({"a": "abc", "b": {"c": "def", "d": 123, "e": "xxx"}})
    json_2 = json.dumps({"a": "tuv", "b": {"c": "ghi", "d": 123}})

    difference = get_diff(json_1, json_2)
    expected_difference = {
        "a": ("abc", "tuv"),
        "b": {"c": ("def", "ghi"), "e": ("xxx", sentinel)},
    }
    assert difference == expected_difference


def test_get_diff_finds_differences_in_nested_pydantic_objects():
    class SomeNestedClass(BaseModel):
        c: str
        d: int
        e: Optional[str]

    class SomeClass(BaseModel):
        a: str
        b: SomeNestedClass

    obj_1 = SomeClass(a="abc", b=SomeNestedClass(c="def", d=123, e="xxx"))
    obj_2 = SomeClass(a="tuv", b=SomeNestedClass(c="ghi", d=123))

    difference = get_diff(obj_1, obj_2)
    expected_difference = {
        "a": ("abc", "tuv"),
        "b": {"c": ("def", "ghi"), "e": ("xxx", None)},
    }
    assert difference == expected_difference


def test_get_diff_finds_matching_substrings_in_nested_dictionaries_if_matching_substrings_arguments_passed():
    first_dict = {
        "id": "12345",
        "location": {
            "street_name": "Totally real street name",
            "street_number": "27",
        },
        "description": {
            "en": None,
            "de": "Some really long description that is different.",
        },
    }

    second_dict = {
        "id": "12845",
        "location": {
            "street_name": "Totally real street name st",
            "street_number": "27",
        },
        "description": {
            "en": None,
            "de": "Some really long description that is different",
        },
    }

    difference = get_diff(first_dict, second_dict, matching_substrings=True)

    expected_difference = {
        "id": [("12", "12"), ("3", "8"), ("45", "45")],
        "location": {
            "street_name": [
                ("Totally real street name", "Totally real street name"),
                ("", " st"),
            ],
        },
        "description": {
            "de": [
                (
                    "Some really long description that is different",
                    "Some really long description that is different",
                ),
                (".", ""),
            ]
        },
    }

    assert difference == expected_difference


def test_main():
    expected_body = {
        "uid": "54ea99ab-fa4c-4fc9-b586-0a6e7fb09793",
        "created_at": "2022-05-10T14:00:10.961047+00:00",
        "updated_at": "2022-10-25T15:15:33.075228+00:00",
        "location": {
            "address": "Some address",
            "street_name": "Totally real street name",
            "street_number": "27",
            "city": "Berlin",
            "country_code": "de",
            "postal_code": "10179",
        },
        "logo_url": "https://logos_r_us.com/123",
        "description": {
            "en": None,
            "de": "Some really long description that is a little different to the second one",
        },
        "language": "de",
        "posting_publish_time": "2022-06-10T14:01:11.969763+00:00",
        "source": None,
        "first_name": "Pretty",
        "last_name": "Good",
        "middle_name": "Decent",
        "age": 99,
    }

    actual = {
        "uid": "59cc1582-ed76-40cd-9a21-25802129b3b5",
        "created_at": "2023-05-10T14:00:10.961047+00:00",
        "updated_at": "2022-10-25T15:15:33.075229+00:00",
        "location": {
            "address": "Some address",
            "street_name": "Totally real street name st",
            "street_number": "27",
            "city": "Berlin",
            "country_code": "de",
            "postal_code": "10179",
        },
        "logo_url": "https://logos_r_us.com/88",
        "description": {
            "en": None,
            "de": "Some really long description that is different to the first one",
        },
        "language": "de",
        "posting_publish_time": "2022-06-10T14:01:11.969763+00:00",
        "source": None,
        "first_name": "Pretty",
        "last_name": "Good",
        "middle_name": "Decent",
        "age": 99,
    }
    show_diff(actual, expected_body)
