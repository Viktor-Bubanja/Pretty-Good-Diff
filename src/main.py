import json
from pydantic import BaseModel
from typing import Optional


def get_dict_diff(first_dict: dict, second_dict: dict, output_dict: Optional[dict] = None, sentinel = object()) -> dict:
    if output_dict is None:
        output_dict = {}

    for key in set(first_dict.keys()) | set(second_dict.keys()):
        first_value = first_dict.get(key, sentinel)
        second_value = second_dict.get(key, sentinel)

        if first_value != second_value:
            if isinstance(first_value, dict) and isinstance(second_value, dict):
                output_dict[key] = {}
                output_dict[key] = get_dict_diff(first_value, second_value, output_dict[key], sentinel)
            else:
                output_dict[key] = (first_value, second_value)

    return output_dict


def get_diff(first_object, second_object, sentinel = object()):
    input_type = type(first_object)
    assert input_type == type(second_object)

    if input_type == dict:
        first_dict, second_dict = first_object, second_object
    elif isinstance(first_object, BaseModel):
        first_dict, second_dict = first_object.dict(), second_object.dict()
    elif input_type == str:  # TODO: check if input str is JSON, if not, compare strings
        first_dict, second_dict = json.loads(first_object), json.loads(second_object)
    else:
        raise NotImplementedError

    return get_dict_diff(first_dict, second_dict, {}, sentinel)
