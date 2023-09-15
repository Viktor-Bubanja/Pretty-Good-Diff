from json import loads
from json.decoder import JSONDecodeError

from src.output import output
from src.sentinel import sentinel
from src.str_diff import get_diff as get_str_diff


def show_diff(first_object, second_object):
    """
    Given two objects of the same type, print the differences between them.
    """
    diff = get_diff(first_object, second_object)
    output(first_object, second_object, diff)


def get_diff(first_object, second_object):
    """
    Given two objects of the same type, return the differences between them.
    """
    input_type = type(first_object)
    assert input_type == type(second_object)

    if input_type == dict:
        return _get_dict_diff(first_object, second_object, {})
    elif input_type == str:
        # Since strings like '123' are converted to ints by json.loads and
        # we want to avoid passing ints to _get_dict_diff, we perform this check
        # first so we can use get_str_diff instead.
        if first_object.isnumeric() or second_object.isnumeric():
            return get_str_diff(first_object, second_object)
        try:
            first_dict, second_dict = loads(first_object), loads(second_object)
            return _get_dict_diff(first_dict, second_dict, {})
        except JSONDecodeError:
            return get_str_diff(first_object, second_object)
    else:
        raise NotImplementedError


def _get_dict_diff(first_dict, second_dict, output_dict):
    if output_dict is None:
        output_dict = {}

    for key in set(first_dict.keys()) | set(second_dict.keys()):
        first_value = first_dict.get(key, sentinel)
        second_value = second_dict.get(key, sentinel)

        if first_value != second_value:
            if isinstance(first_value, dict) and isinstance(second_value, dict):
                output_dict[key] = {}
                output_dict[key] = _get_dict_diff(
                    first_value, second_value, output_dict[key]
                )
            elif isinstance(first_value, str) and isinstance(second_value, str):
                output_dict[key] = get_str_diff(first_value, second_value)
            else:
                output_dict[key] = (first_value, second_value)
    return output_dict
