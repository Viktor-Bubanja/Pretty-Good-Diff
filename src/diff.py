from json import loads
from json.decoder import JSONDecodeError
from pydantic import BaseModel
from typing import Optional
from src.output import output
from src.sentinel import sentinel


def print_diff(first_object, second_object):
    diff = get_diff(first_object, second_object)
    output(diff)


def get_diff(first_object, second_object):
    input_type = type(first_object)
    assert input_type == type(second_object)

    if input_type == dict:
        first_dict, second_dict = first_object, second_object
    elif isinstance(first_object, BaseModel):
        first_dict, second_dict = first_object.dict(), second_object.dict()
    elif input_type == str:
        try:
            first_dict, second_dict = loads(first_object), loads(second_object)
        except JSONDecodeError:
            return _get_str_diff(first_object, second_object)
    else:
        raise NotImplementedError

    return _get_dict_diff(first_dict, second_dict, {})


def _get_dict_diff(first_dict: dict, second_dict: dict, output_dict: Optional[dict] = None) -> dict:
    if output_dict is None:
        output_dict = {}

    for key in set(first_dict.keys()) | set(second_dict.keys()):
        first_value = first_dict.get(key, sentinel)
        second_value = second_dict.get(key, sentinel)

        if first_value != second_value:
            if isinstance(first_value, dict) and isinstance(second_value, dict):
                output_dict[key] = {}
                output_dict[key] = _get_dict_diff(first_value, second_value, output_dict[key])
            else:
                output_dict[key] = (first_value, second_value)

    return output_dict


def _get_str_diff(first_str: str, second_str: str) -> str:
    output = []
    previously_matching = first_str[0] == second_str[0]
    sub_strings = ["", ""]
    for x, y in zip(first_str, second_str):
        matching = x == y

        if matching and previously_matching:
            sub_strings[0] += x
            sub_strings[1] += y
        elif not matching and not previously_matching:
            sub_strings[0] += x
            sub_strings[1] += y
        else:
            output.append(sub_strings)
            sub_strings = [x, y]

        previously_matching = x == y
    output.append(sub_strings)
    return output
