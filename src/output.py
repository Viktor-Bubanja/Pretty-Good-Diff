from src.sentinel import sentinel

INDENT_SIZE = 4


def output(first_object, second_object, diff, matching_substrings=False):
    print(
        f"\n{_blue_background_output('actual')} vs {_purple_background_output('expected')}\n\n"
    )
    if type(diff) == dict:
        output_dict_diff(diff, 0, matching_substrings)
    if type(diff) == list:
        output_str_diff(first_object, second_object, diff)


def output_dict_diff(output_dict: dict, indent=0, matching_substrings=False) -> None:
    missing_message = _red_output("<missing>")

    for key, value in output_dict.items():
        if type(value) == dict:
            print(indent * " " + _yellow_output(key))
            output_dict_diff(value, (indent + INDENT_SIZE), matching_substrings)
        else:
            # if matching_substrings:
            #     breakpoint()
            #     output_str_diff(value)
            # else:
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


def output_str_diff(first_object, second_object, substrings: list) -> None:
    diff = ""
    first_obj_mappings, second_object_mappings = [sub[0] for sub in substrings], [
        sub[1] for sub in substrings
    ]

    previous_first_index = -1
    previous_second_index = -1
    for x, y in zip(first_obj_mappings, second_object_mappings):
        if x[0] > previous_first_index:
            diff += _blue_background_output(
                first_object[slice(previous_first_index + 1, x[0])]
            )
        if y[0] > previous_second_index:
            diff += _purple_background_output(
                second_object[slice(previous_second_index + 1, y[0])]
            )
        diff += first_object[slice(x[0], x[-1] + 1)]
        previous_first_index = x[-1]
        previous_second_index = y[-1]

    print(diff)


def _yellow_output(value):
    return _colored_output(value, "93m")


def _purple_background_output(value):
    return _colored_output(value, "45m")


def _blue_background_output(value):
    return _colored_output(value, "44m")


def _red_output(value):
    return _colored_output(value, "31m")


def _pale_green_output(value):
    return _colored_output(value, "92m")


def _colored_output(value, color_symbol):
    return f"\033[{color_symbol}{value}\033[00m"


output_str_diff("Y123345", "1288845W", [[[1, 2], [0, 1]], [[5, 6], [5, 6]]])
