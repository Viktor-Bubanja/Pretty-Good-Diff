from src.sentinel import sentinel
INDENT_SIZE = 4


def output(diff):
    print(f"\n{_blue_output('actual')} vs {_purple_output('expected')}\n\n")
    if type(diff) == dict:
        output_dict_diff(diff)
    if type(diff) == list:
        output_str_diff(diff)


def output_dict_diff(output_dict: dict, indent = 0) -> None:
    missing_message = _red_output("<missing>")

    for key, value in output_dict.items():
        if type(value) == dict:
            print(indent * " " + _yellow_output(key))
            output_dict_diff(value, (indent + INDENT_SIZE))
        else:
            first_obj, second_obj = value
            actual_output = missing_message if first_obj is sentinel else _blue_output(first_obj)
            expected_output = missing_message if second_obj is sentinel else _purple_output(second_obj)

            out_string = "{}: {} {}".format(_yellow_output(key), actual_output, expected_output)
            print(indent * " " + out_string)


def output_str_diff(substrings: list) -> None:
    diff = ""
    for first_sub, second_sub in substrings:
        if first_sub == second_sub:
            diff += _pale_green_output(first_sub)
        else:
            diff += f"{_blue_output(first_sub)}{_purple_output(second_sub)}"
    print(diff)


def _yellow_output(value):
    return _colored_output(value, "93m")


def _purple_output(value):
    return _colored_output(value, "95m")


def _blue_output(value):
    return _colored_output(value, "96m")


def _red_output(value):
    return _colored_output(value, "31m")


def _pale_green_output(value):
    return _colored_output(value, "91m")


def _colored_output(value, color_symbol):
    return f"\033[{color_symbol}{value}\033[00m"
