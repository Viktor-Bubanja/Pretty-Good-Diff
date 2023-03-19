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
                for existing_substring in output:
                    if set(existing_substring[1][0]) & set(substrings[1][0]) or set(existing_substring[1][1]) & set(substrings[1][1]) and len(existing_substring[0]) < len(substrings[0]):
                        output.remove(existing_substring)
                add = True
                for existing_substring in output:
                    if (
                            set(existing_substring[1][0]) & set(substrings[1][0]) or set(existing_substring[1][1]) & set(substrings[1][1])
                        ) and len(existing_substring[0]) > len(substrings[0]):
                        add = False
                i_first = 0
                first_str_done = True
                matching = False
                if add:
                    output.append(substrings)
                substrings = ["", [[], []]]
            elif i_second == len(second_str) and not second_str_done:
                for existing_substring in output:
                    if (
                            set(existing_substring[1][0]) & set(substrings[1][0]) or set(existing_substring[1][1]) & set(substrings[1][1])
                        ) and len(existing_substring[0]) < len(substrings[0]):
                        output.remove(existing_substring)
                add = True
                for existing_substring in output:
                    if (set(existing_substring[1][0]) & set(substrings[1][0]) or set(existing_substring[1][1]) & set(substrings[1][1])
                        ) or (existing_substring[1][0][0] < substrings[1][0][0] and existing_substring[1][1][0] > substrings[1][1][0]
                        ) or (existing_substring[1][0][0] > substrings[1][0][0] and existing_substring[1][1][0] < substrings[1][1][0]
                        ) and len(existing_substring[0]) > len(substrings[0]):
                        add = False
                i_second = 0
                second_str_done = True
                matching = False
                if add:
                    output.append(substrings)
                substrings = ["", [[], []]]
        elif x != y and previously_matching:
            for existing_substring in output:
                if (
                        set(existing_substring[1][0]) & set(substrings[1][0]) or set(existing_substring[1][1]) & set(substrings[1][1])
                    ) and len(existing_substring[0]) < len(substrings[0]):
                    output.remove(existing_substring)
            add = True
            for existing_substring in output:
                if (
                        set(existing_substring[1][0]) & set(substrings[1][0]) or set(existing_substring[1][1]) & set(substrings[1][1])
                    ) and len(existing_substring[0]) > len(substrings[0]):
                    add = False
            i_second = 0
            if add:
                output.append(substrings)
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
    add = True
    for existing_substring in output:
        if (
                (existing_substring[1][0][-1] < i_first - 1 and existing_substring[1][1][0] > i_second - 1) or
                (existing_substring[1][0][0] > i_first - 1 and existing_substring[1][1][-1] < i_second - 1)
            ) and len(existing_substring[0]) < len(substrings[0]):
            add = False
    if add and substrings[0] and substrings not in output:
        output.append(substrings)
    print(output)


get_diff("SAMATY", "SAMSAMANTH")
