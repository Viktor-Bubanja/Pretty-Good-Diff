"""
These tests do not have any assertions, they are just used to manually check
what the output looks like.
"""
from pretty_good_diff.output import show_diff


def test_output_with_string_difference():
    first_str = "Some really long string that has a couple of differences."
    second_str = "Some rlly long string thathas a couple of differences."
    show_diff(first_str, second_str)


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
            "de": "Some really long description that is different. How am I meant to see that a full stop is missing if it's not red?",
        },
        "summary": "Some verbose text that is identical in both texts and definitely doesn't need to be displayed in the output.",
    }
    second_dict = {
        "id": "12845",
        "location": {
            "street_name": "Totally real st name",
            "street_number": "27",
        },
        "description": {
            "en": None,
            "de": "Some really really long description that is different How am I meant to see that a full stop is missing if it's not red?",
        },
        "summary": "Some verbose text that is identical in both texts and definitely doesn't need to be displayed in the output.",
    }
    show_diff(first_dict, second_dict)
