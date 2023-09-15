"""
These tests do not have any assertions, they are just used to manually check
what the output looks like.
"""
from src.diff import get_diff
from src.output import output


def test_output_with_string_difference():
    first_str = "Some really long string that has a couple of differences."
    second_str = "Some rlly long string thathas a couple of differences."
    difference = get_diff(first_str, second_str)
    output(first_str, second_str, difference)


def test_output_with_nested_dictionary_with_string_difference():
    first_dict = {
        "id": "12345",
        "location": {
            "street_name": "Totally real street name",
            "street_number": "27",
            "city": "Berlin",
        },
        "description": {
            "en": None,
            "de": "Some really long description that is different.",
        },
    }

    second_dict = {
        "id": "12845",
        "location": {
            "street_name": "Totally real st name",
            "street_number": "27",
        },
        "description": {
            "en": None,
            "de": "Some really really long description that is different",
        },
    }

    diff = get_diff(first_dict, second_dict)
    output(first_dict, second_dict, diff)
