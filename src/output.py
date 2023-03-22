from src.sentinel import sentinel
INDENT_SIZE = 4


def output(diff, matching_substrings = False):
    print(f"\n{_blue_output('actual')} vs {_purple_output('expected')}\n\n")
    if type(diff) == dict:
        output_dict_diff(diff, 0, matching_substrings)
    if type(diff) == list:
        output_str_diff(diff, 0, matching_substrings)


def output_dict_diff(output_dict: dict, indent = 0, matching_substrings = False) -> None:
    missing_message = _red_output("<missing>")

    for key, value in output_dict.items():
        if type(value) == dict:
            print(indent * " " + _yellow_output(key))
            output_dict_diff(value, (indent + INDENT_SIZE), matching_substrings)
        else:
            if matching_substrings:
                output_str_diff(value)
            else:
                first_obj, second_obj = value
                actual_output = missing_message if first_obj is sentinel else _blue_output(first_obj)
                expected_output = missing_message if second_obj is sentinel else _purple_output(second_obj)

                out_string = "{}: {} {}".format(_yellow_output(key), actual_output, expected_output)
                print(indent * " " + out_string)


def output_dict_diff2(output_dict: dict, indent = 0) -> None:
    missing_message = _red_output("<missing>")

    for key, value in output_dict.items():
        if type(value) == dict:
            print(indent * " " + _yellow_output(key))
            output_dict_diff2(value, (indent + INDENT_SIZE))
        else:
            output_str_diff(value)

def output_str_diff(first_object, second_object, substrings: list) -> None:
    breakpoint()
    diff = ""
    mapped_indices_from_first_obj = set(chain(*[sub[1][0] for sub in substrings]))

    for i, (x, y) in enumerate(zip_longest(first_object, second_object)):
        if i in mapped_indices_from_first_obj:
            diff += _pale_green_output(x)
        else:
            if x:
                diff += _blue_output(x)
            if y:
                diff += _purple_output(y)

    print(diff)


def alternating_matching_and_unmatching_substrings(first_object, second_object, substrings: list) -> list:
    mapped_indices_from_first_obj = [sub[1][0] for sub in substrings]
    unmapped_indices_from_first_obj = []
    previous_mapping = mapped_indices_from_first_obj[0]
    for mapping in mapped_indices_from_first_obj:
        start_index = previous_mapping[-1] + 1 if unmapped_indices_from_first_obj else 0
        unmapped = list(range(start_index, mapping[0]))
        previous_mapping = mapping
        unmapped_indices_from_first_obj.append(unmapped)
    if unmapped_indices_from_first_obj[-1][-1] < len(second_object):
        unmapped_indices_from_first_obj.append(list(range(mapped_indices_from_first_obj[-1][-1] + 1, len(first_object))))
    print(unmapped_indices_from_first_obj)

    mapped_indices_from_second_obj = [sub[1][1] for sub in substrings]
    unmapped_indices_from_second_obj = []
    previous_mapping = mapped_indices_from_second_obj[0]
    for mapping in mapped_indices_from_second_obj:
        start_index = previous_mapping[-1] + 1 if unmapped_indices_from_second_obj else 0
        unmapped = list(range(start_index, mapping[0]))
        previous_mapping = mapping
        unmapped_indices_from_second_obj.append(unmapped)
    if unmapped_indices_from_second_obj[-1][-1] < len(second_object):
        unmapped_indices_from_second_obj.append(list(range(mapped_indices_from_second_obj[-1][-1] + 1, len(second_object))))
    print(unmapped_indices_from_second_obj)

alternating_matching_and_unmatching_substrings("Y123345", "1288845W", [['12', [[1, 2], [0, 1]]], ['45', [[5, 6], [5, 6]]]])

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
