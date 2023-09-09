from src.sentinel import sentinel

INDENT_SIZE = 4


def output(first_object, second_object, diff, matching_substrings=False):
    print(
        f"\n{_blue_background_output('actual')} vs {_purple_background_output('expected')}\n\n"
    )
    if type(diff) == dict:
        output_dict_diff(diff, 0, matching_substrings)
    if type(diff) == list:
        output_str_diff(diff)


def output_dict_diff(
    output_dict: dict, indent: int = 0, matching_substrings: bool = False
) -> None:
    missing_message = _red_output("<missing>")

    for key, value in output_dict.items():
        if type(value) == dict:
            print(indent * " " + _yellow_output(key))
            output_dict_diff(value, (indent + INDENT_SIZE), matching_substrings)
        else:
            if matching_substrings:
                print(indent * " " + _yellow_output(key))
                output_str_diff(value, indent=indent + INDENT_SIZE)
            else:
                first_obj, second_obj = value
                actual_output = (
                    missing_message
                    if first_obj is sentinel
                    else _blue_background_output(first_obj)
                )
                expected_output = (
                    missing_message
                    if second_obj is sentinel
                    else _purple_background_output(second_obj)
                )

                out_string = "{}: {} {}".format(
                    _yellow_output(key), actual_output, expected_output
                )
                print(indent * " " + out_string)


def output_str_diff(substring_pairs: list, indent: int = 0) -> None:
    diff = " " * indent
    for substring_1, substring_2 in substring_pairs:
        if substring_1 == substring_2:
            diff += _pale_green_output(substring_1)
        else:
            diff += _red_output(substring_1)
    print(diff)
    diff = " " * indent
    for substring_1, substring_2 in substring_pairs:
        if substring_1 == substring_2:
            diff += _pale_green_output(substring_2)
        else:
            diff += _purple_output(substring_2)
    print(diff)


def _yellow_output(value):
    return _colored_output(value, "93m")


def _purple_background_output(value):
    return _colored_output(value, "45m")


def _blue_background_output(value):
    return _colored_output(value, "44m")


def _purple_output(value):
    return _colored_output(value, "35m")


def _red_output(value):
    return _colored_output(value, "31m")


def _pale_green_output(value):
    return _colored_output(value, "92m")


def _colored_output(value, color_symbol):
    return f"\033[{color_symbol}{value}\033[00m"
