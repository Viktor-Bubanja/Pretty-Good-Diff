from src.colors import *
from src.sentinel import sentinel

INDENT_SIZE = 4


def output(diff, matching_substrings=False):
    """
    Given the difference between two objects, output the difference to the console.
    If matching_substrings is False, when comparing two different strings, it will print both
    objects. When matching_substrings is True, it will print one string where the differences
    between the two strings are highlighted.
    """
    print(
        f"\n{_colored_output('actual', BLUE_BACKGROUND)} vs {_colored_output('expected', PURPLE_BACKGROUND)}\n\n"
    )
    if type(diff) == dict:
        output_dict_diff(diff, 0, matching_substrings)
    if type(diff) == list:
        output_str_diff(diff)


def output_dict_diff(output_dict, indent=0, matching_substrings=False):
    missing_message = _colored_output("<missing>", RED)

    for key, value in output_dict.items():
        if type(value) == dict:
            print(indent * " " + _colored_output(key, YELLOW))
            output_dict_diff(value, (indent + INDENT_SIZE), matching_substrings)
        else:
            if matching_substrings:
                print(indent * " " + _colored_output(key, YELLOW))
                output_str_diff(value, indent=indent + INDENT_SIZE)
            else:
                first_obj, second_obj = value
                actual_output = (
                    missing_message
                    if first_obj is sentinel
                    else _colored_output(first_obj, BLUE_BACKGROUND)
                )
                expected_output = (
                    missing_message
                    if second_obj is sentinel
                    else _colored_output(second_obj, PURPLE_BACKGROUND)
                )

                out_string = "{}: {} {}".format(
                    _colored_output(key, YELLOW), actual_output, expected_output
                )
                print(indent * " " + out_string)


def output_str_diff(substring_pairs, indent=0):
    diff = " " * indent
    for substring_1, substring_2 in substring_pairs:
        if substring_1 == substring_2:
            diff += _colored_output(substring_1, PALE_GREEN)
        else:
            diff += _colored_output(substring_1, RED)
    print(diff)
    diff = " " * indent
    for substring_1, substring_2 in substring_pairs:
        if substring_1 == substring_2:
            diff += _colored_output(substring_2, PALE_GREEN)
        else:
            diff += _colored_output(substring_2, PURPLE)
    print(diff)


def _colored_output(value, color_symbol):
    return f"\033[{color_symbol}{value}\033[00m"
