def get_diff(first_str: str, second_str: str) -> list[str]:
    i_first, i_second = 0, 0
    output = []
    substrings = ["", [[], []]]
    previously_matching = first_str[i_first] == second_str[i_second]
    first_str_done = second_str_done = False

    while i_first < len(first_str) and i_second < len(second_str):
        x, y = first_str[i_first], second_str[i_second]
        matching = x == y
        if matching and previously_matching:
            substrings[0] += x
            substrings[1][0].append(i_first)
            substrings[1][1].append(i_second)
            i_first += 1
            i_second += 1
            if i_first == len(first_str) and not first_str_done:
                if worse_substring := worse_overlapping_substring(output, substrings):
                    output.remove(worse_substring)
                if not better_overlapping_substring(output, substrings):
                    output.append(substrings)
                i_first = 0
                first_str_done = True
                matching = False
                substrings = ["", [[], []]]
            elif i_second == len(second_str) and not second_str_done:
                if worse_substring := worse_overlapping_substring(output, substrings):
                    output.remove(worse_substring)
                if not better_overlapping_substring(output, substrings):
                    output.append(substrings)
                i_second = 0
                second_str_done = True
                matching = False
                substrings = ["", [[], []]]
        elif x != y and previously_matching:
            if worse_substring := worse_overlapping_substring(output, substrings):
                output.remove(worse_substring)
            if not better_overlapping_substring(output, substrings):
                output.append(substrings)
            i_second = 0
            substrings = ["", [[], []]]
        elif x != y and not previously_matching:
            if i_second < len(second_str) - 1:
                i_second += 1
            elif i_first < len(first_str) - 1:
                i_first += 1
                i_second = 0
            else:
                break
        previously_matching = matching

    if substrings[0] and not better_overlapping_substring(output, substrings) and substrings not in output:
        output.append(substrings)

    print(output)


def better_overlapping_substring(output, substring):
    return overlapping_substring(output, substring, lambda x, y: x > y)


def worse_overlapping_substring(output, substring):
    return overlapping_substring(output, substring, lambda x, y: x < y)


def overlapping_substring(output, substring, func):
    sub, _ = substring
    for existing_substring in output:
        existing_sub, _ = existing_substring
        if func(len(existing_sub), len(sub)) and substrings_overlap(existing_substring, substring):
            return existing_substring

    return None 


def substrings_overlap(existing_substring, substring):
    _, sub_mapping = substring
    _, existing_mapping = existing_substring
    if (set(existing_mapping[0]) & set(sub_mapping[0]) or set(existing_mapping[1]) & set(sub_mapping[1])
    ) or (existing_mapping[0][0] < sub_mapping[0][0] and existing_mapping[1][0] > sub_mapping[1][0]
    ) or (existing_mapping[0][0] > sub_mapping[0][0] and existing_mapping[1][0] < sub_mapping[1][0]
    ):
        return existing_substring
            



get_diff("SAMAT", "SAMSAMAN")
# get_diff("12345", "12845")
