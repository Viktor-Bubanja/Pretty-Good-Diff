from typing import Optional


def get_diff(first_dict: dict, second_dict: dict, output_dict: Optional[dict] = None, sentinel = None) -> dict:
    if output_dict is None:
        output_dict = {}

    for key in set(first_dict.keys()) | set(second_dict.keys()):
        first_value = first_dict.get(key, sentinel)
        second_value = second_dict.get(key, sentinel)

        if first_value != second_value:
            if isinstance(first_value, dict) and isinstance(second_value, dict):
                output_dict[key] = {}
                output_dict[key] = get_diff(first_value, second_value, output_dict[key], sentinel)
            else:
                output_dict[key] = (first_value, second_value)

    return output_dict
