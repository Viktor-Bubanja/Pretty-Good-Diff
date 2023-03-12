def output(output_dict: dict, sentinel = object()) -> None:
    print(f"{_blue_output('actual')} =={_purple_output('expected')}\n\n")

    missing_message = _red_output("<missing>")

    for key, (actual, expected) in output_dict.items():
        actual_output = missing_message if actual == sentinel else _blue_output(actual)
        expected_output = missing_message if expected == sentinel else _purple_output(expected)

        out_string = "{}:{},{}".format(_yellow_output(key), actual_output, expected_output)
        print(out_string)


def _yellow_output(value):
    return f"\033[93m {value}\033[00m"


def _purple_output(value):
    return f"\033[95m {value}\033[00m"


def _blue_output(value):
    return f"\033[96m {value}\033[00m"


def _red_output(value):
    return f"\033[31m {value}\033[00m"
