from pretty_good_diff.colors import *
from pretty_good_diff.diff import get_diff
from pretty_good_diff.sentinel import sentinel

INDENT_SIZE = 4


def show_diff(first_object, second_object):
    """
    Given two objects of the same type, print the differences between them.
    """
    diff = get_diff(first_object, second_object)
    if not diff or first_object == second_object:
        print(f"\n{_colored_output('The two objects are identical.', PALE_GREEN)}\n")
    elif type(diff) == dict:
        _output_dict_diff(first_object, second_object, diff, 0)
    elif type(diff) == list:
        _output_str_diff(first_object, second_object, diff)


def _output_dict_diff(first_object, second_object, diff, indent=0):
    missing_message = _colored_output("<missing>", RED)
    for key, value in diff.items():
        if type(value) == dict:
            print(indent * " " + _colored_output(key, YELLOW))
            _output_dict_diff(
                first_object[key], second_object[key], value, (indent + INDENT_SIZE)
            )
        elif type(value) == list:
            print(indent * " " + _colored_output(key, YELLOW))
            _output_str_diff(
                first_object[key],
                second_object[key],
                value,
                indent=indent + INDENT_SIZE,
            )
        else:
            print(indent * " " + _colored_output(key, YELLOW))
            indent_for_values = indent + INDENT_SIZE
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
            print(indent_for_values * " " + actual_output)
            print(indent_for_values * " " + expected_output)


def _output_str_diff(first_str, second_str, index_pairs, indent=0):
    first_str_indexes, second_str_indexes = zip(*index_pairs)
    print(_get_coloured_diff(first_str, first_str_indexes, indent))
    print(
        _get_coloured_diff(
            second_str, second_str_indexes, indent, unmatched_colour=PURPLE
        )
    )


def _get_coloured_diff(string, index_pairs, indent=0, unmatched_colour=RED):
    diff = "" + " " * indent
    for i in range(len(string)):
        if i in index_pairs:
            diff += _colored_output(string[i], PALE_GREEN)
        else:
            diff += _colored_output(string[i], unmatched_colour)
    return diff


def _colored_output(value, color_symbol):
    return f"\033[{color_symbol}{value}\033[00m"
