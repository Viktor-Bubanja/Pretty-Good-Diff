def get_diff(first_str: str, second_str: str) -> list[str]:
    first_option = _calculate_diff(first_str, second_str)
    second_option = _calculate_diff(second_str, first_str)

    def len_matching_substrings(substrings):
        return sum([len(sub[0]) for sub in substrings])

    if len_matching_substrings(first_option) > len_matching_substrings(second_option):
        return first_option
    else:
        second_option = [(sub[1], sub[0]) for sub in second_option]
        return second_option


def _calculate_diff(first_str: str, second_str: str) -> list[str]:
    i_first, i_second = 0, 0
    output = []
    mappings = ([], [])
    previously_matching = first_str[i_first] == second_str[i_second]
    first_str_done = second_str_done = False

    while i_first < len(first_str) and i_second < len(second_str):
        x, y = first_str[i_first], second_str[i_second]
        matching = x == y
        if matching and previously_matching:
            mappings[0].append(i_first)
            mappings[1].append(i_second)
            i_first += 1
            i_second += 1
            if i_first == len(first_str) and not first_str_done:
                if worse_substring := _worse_overlapping_substring(output, mappings):
                    output.remove(worse_substring)
                if not _better_overlapping_substring(output, mappings):
                    output.append(mappings)
                i_first = 0
                first_str_done = True
                matching = False
                mappings = ([], [])
            elif i_second == len(second_str) and not second_str_done:
                if worse_substring := _worse_overlapping_substring(output, mappings):
                    output.remove(worse_substring)
                if not _better_overlapping_substring(output, mappings):
                    output.append(mappings)
                i_second = 0
                second_str_done = True
                matching = False
                mappings = ([], [])
        elif not matching and previously_matching:
            if worse_substring := _worse_overlapping_substring(output, mappings):
                output.remove(worse_substring)
            if not _better_overlapping_substring(output, mappings):
                output.append(mappings)
            i_second = 0
            matching = False
            mappings = ([], [])
        elif not matching and not previously_matching:
            matching = False
            if i_second < len(second_str) - 1:
                i_second += 1
            elif i_first < len(first_str) - 1:
                i_first += 1
                i_second = 0
            else:
                break
        previously_matching = matching

    if not _better_overlapping_substring(output, mappings) and mappings not in output:
        output.append(mappings)

    if output and output[-1] == ([], []):
        output = output[:-1]

    return output


def _better_overlapping_substring(output, substring):
    return _overlapping_substring(output, substring, lambda x, y: x >= y)


def _worse_overlapping_substring(output, substring):
    return _overlapping_substring(output, substring, lambda x, y: x < y)


def _overlapping_substring(output, substring, func):
    sub, _ = substring
    for existing_substring in output:
        existing_sub, _ = existing_substring
        if func(len(existing_sub), len(sub)) and _mappings_overlap(
            existing_substring, substring
        ):
            return existing_substring

    return None


def _mappings_overlap(existing_mapping, new_mapping):
    if not new_mapping[0] or not new_mapping[1]:
        return False
    if (
        (
            set(existing_mapping[0]) & set(new_mapping[0])
            or set(existing_mapping[1]) & set(new_mapping[1])
        )
        or (
            existing_mapping[0][0] < new_mapping[0][0]
            and existing_mapping[1][0] > new_mapping[1][0]
        )
        or (
            existing_mapping[0][0] > new_mapping[0][0]
            and existing_mapping[1][0] < new_mapping[1][0]
        )
    ):
        return True
