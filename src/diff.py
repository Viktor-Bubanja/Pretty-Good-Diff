from json import loads
from json.decoder import JSONDecodeError
from typing import Optional

from pydantic import BaseModel

from src.output import output
from src.sentinel import sentinel
from src.str_diff import get_diff as get_str_diff


def print_diff(first_object, second_object, matching_substrings=False):
    diff = get_diff(first_object, second_object, matching_substrings)
    output(first_object, second_object, diff, matching_substrings)


def get_diff(first_object, second_object, matching_substrings=False):
    input_type = type(first_object)
    assert input_type == type(second_object)

    if input_type == dict:
        first_dict, second_dict = first_object, second_object
    elif isinstance(first_object, BaseModel):
        first_dict, second_dict = first_object.dict(), second_object.dict()
    elif input_type == str:
        if first_object.isnumeric() or second_object.isnumeric():
            return get_str_diff(first_object, second_object)
        try:
            first_dict, second_dict = loads(first_object), loads(second_object)
        except JSONDecodeError:
            return get_str_diff(first_object, second_object)
    else:
        raise NotImplementedError

    return _get_dict_diff(first_dict, second_dict, {}, matching_substrings)


def _get_dict_diff(
    first_dict: dict,
    second_dict: dict,
    output_dict: Optional[dict] = None,
    matching_substrings=False,
) -> dict:
    if output_dict is None:
        output_dict = {}

    for key in set(first_dict.keys()) | set(second_dict.keys()):
        first_value = first_dict.get(key, sentinel)
        second_value = second_dict.get(key, sentinel)

        if first_value != second_value:
            if isinstance(first_value, dict) and isinstance(second_value, dict):
                output_dict[key] = {}
                output_dict[key] = _get_dict_diff(
                    first_value, second_value, output_dict[key], matching_substrings
                )
            else:
                output_dict[key] = (
                    get_str_diff(first_value, second_value)
                    if matching_substrings
                    else (first_value, second_value)
                )

    return output_dict
