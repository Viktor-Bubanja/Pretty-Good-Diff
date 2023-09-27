from json import loads
from json.decoder import JSONDecodeError

from src.exceptions import InputTypesMismatchError
from src.sentinel import sentinel


def get_diff(first_object, second_object):
    """
    Given two objects of the same type, return an internal representation of the differences between them.
    """
    if type(first_object) is not type(second_object):
        raise InputTypesMismatchError(
            "The types of the two input objects must be the same"
        )

    input_type = type(first_object)
    if input_type == dict:
        return _get_dict_diff(first_object, second_object, {})
    elif input_type == str:
        # Since strings like '123' are converted to ints by json.loads and
        # we want to avoid passing ints to _get_dict_diff, we perform this check
        # first so we can use get_str_diff instead.
        if first_object.isnumeric() or second_object.isnumeric():
            return _get_str_diff(first_object, second_object)
        try:
            first_dict, second_dict = loads(first_object), loads(second_object)
            return _get_dict_diff(first_dict, second_dict, {})
        except JSONDecodeError:
            return _get_str_diff(first_object, second_object)
    else:
        raise NotImplementedError


def _get_dict_diff(first_dict, second_dict, output_dict):
    """
    Recursively compare two dictionaries and return an internal representation of the differences between them.
    If one dictionary has a key that the other doesn't, the key is added to the output dictionary with the value.
    """
    if output_dict is None:
        output_dict = {}

    for key in set(first_dict.keys()) | set(second_dict.keys()):
        first_value = first_dict.get(key, sentinel)
        second_value = second_dict.get(key, sentinel)

        if first_value != second_value:
            if isinstance(first_value, dict) and isinstance(second_value, dict):
                output_dict[key] = {}
                output_dict[key] = _get_dict_diff(
                    first_value, second_value, output_dict[key]
                )
            elif isinstance(first_value, str) and isinstance(second_value, str):
                output_dict[key] = _get_str_diff(first_value, second_value)
            else:
                output_dict[key] = (first_value, second_value)
    return output_dict


def _get_str_diff(first_str, second_str):
    """
    Dynamic programming solution which outputs a list of tuples of indexes which
    map the two strings together. For example, if we have the following two strings:
    first_str: ABCDEFG
    second_str: ABXCDXXFG
    The output would be [(0, 0), (1, 1), (2, 3), (3, 4), (4, 6), (5, 7), (6, 8)]
    """
    if first_str is sentinel or second_str is sentinel:
        return []

    mappings = [
        [[] for _ in range(len(second_str) + 1)] for _ in range(len(first_str) + 1)
    ]
    for i in range(len(first_str)):
        for j in range(len(second_str)):
            if first_str[i] == second_str[j]:
                mappings[i + 1][j + 1] = mappings[i][j] + [(i, j)]
            else:
                mappings[i + 1][j + 1] = max(
                    mappings[i + 1][j], mappings[i][j + 1], key=len
                )
    return _find_best_solution(mappings)


def _find_best_solution(matrix):
    """
    The 'best' solution is the one that maps the highest number of characters together
    between the two strings. Equally good solutions are prioritised by how 'grouped together'
    the mappings are. A further description is given in the docstring of _calculate_separatedness.
    """
    max_value = 0
    separateness_of_best_solution = float("inf")
    max_index = 0, 0

    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if len(matrix[i][j]) >= max_value:
                separateness = _calculate_separatedness(matrix[i][j])
                if len(matrix[i][j]) == max_value:
                    if separateness >= separateness_of_best_solution:
                        continue
                max_value = len(matrix[i][j])
                max_index = (i, j)
                separateness_of_best_solution = separateness

    return matrix[max_index[0]][max_index[1]]


def _calculate_separatedness(mapped_indexes):
    """
    We want to prioritise pairing up indexes so that substrings are grouped together
    as much as possible. For example, if we have the following two strings:
    first_str: AXBXCXABC
    second_str: ABCXXXXX
    We want to map the "ABC" from the end of the first string to the "ABC" in the second string
    instead of mapping each of the letters "A", "B", and "C" individually.
    We therefore have this function to calculate the level of 'separatedness' of a mapping.
    """
    if not mapped_indexes:
        return 0
    first_str_indexes, second_str_indexes = zip(*mapped_indexes)
    return sum(
        first_str_indexes[i + 1] - first_str_indexes[i]
        for i in range(len(first_str_indexes) - 1)
    ) + sum(
        second_str_indexes[i + 1] - second_str_indexes[i]
        for i in range(len(second_str_indexes) - 1)
    )
