from json import loads
from json.decoder import JSONDecodeError
from pydantic import BaseModel
from typing import Optional
# from src.output import output
# from src.sentinel import sentinel


def print_diff(first_object, second_object, matching_substrings = False):
    diff = get_diff(first_object, second_object, matching_substrings)
    output(diff, matching_substrings)


def get_diff(first_object, second_object, matching_substrings = False):
    input_type = type(first_object)
    assert input_type == type(second_object)

    if input_type == dict:
        first_dict, second_dict = first_object, second_object
    elif isinstance(first_object, BaseModel):
        first_dict, second_dict = first_object.dict(), second_object.dict()
    elif input_type == str:
        if first_object.isnumeric() or second_object.isnumeric():
            return _get_str_diff(first_object, second_object)
        try:
            first_dict, second_dict = loads(first_object), loads(second_object)
        except JSONDecodeError:
            return _get_str_diff(first_object, second_object)
    else:
        raise NotImplementedError

    return _get_dict_diff(first_dict, second_dict, {}, matching_substrings)


def _get_dict_diff(first_dict: dict, second_dict: dict, output_dict: Optional[dict] = None, matching_substrings = False) -> dict:
    if output_dict is None:
        output_dict = {}

    for key in set(first_dict.keys()) | set(second_dict.keys()):
        first_value = first_dict.get(key, sentinel)
        second_value = second_dict.get(key, sentinel)

        if first_value != second_value:
            if isinstance(first_value, dict) and isinstance(second_value, dict):
                output_dict[key] = {}
                output_dict[key] = _get_dict_diff(first_value, second_value, output_dict[key], matching_substrings)
            else:
                output_dict[key] = _get_str_diff(first_value, second_value) if matching_substrings else (first_value, second_value)

    return output_dict


def _get_str_diff(first_str: str, second_str: str) -> list[str]:
    first_str_i, second_str_i = 0, 0
    output = []
    substrings = ["", ""]
    matching = True
    previously_matching = first_str[0] == second_str[0]
    first_matched = second_matched = 0
    while (first_matched < len(first_str) or second_matched < len(second_str)) and first_str_i < len(first_str) and second_str_i < len(second_str):
        x, y = first_str[first_str_i], second_str[second_str_i]
        matching = x == y
        if matching and previously_matching:
            first_matched = first_str_i
            second_matched = second_str_i
            substrings[0] += x
            substrings[1] += y
            first_str_i += 1
            second_str_i += 1
        elif not matching and not previously_matching:
            if second_str_i < len(second_str):
                substrings[1] += y
                second_str_i += 1
            elif first_str_i < len(first_str):
                substrings[0] += x
                first_str_i += 1
            elif second_matched < len(second_str):
                second_str_i = second_matched + 1
            elif first_matched < len(first_str):
                first_str_i = first_matched + 1
        else:
            output.append(substrings)
            substrings = ["", ""]
        previously_matching = matching
    output.append([first_str[first_str_i:], ""])
    output.append(substrings)
    
    print(output)

_get_str_diff("12345", "12845")
 