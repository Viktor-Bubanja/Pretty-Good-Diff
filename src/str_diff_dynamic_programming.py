def get_diff(first_str, second_str):
    mappings = [[[] for _ in range(len(second_str) + 1)] for _ in range(len(first_str) + 1)]
    for i in range(len(first_str)):
        for j in range(len(second_str)):
            if first_str[i] == second_str[j]:
                mappings[i + 1][j + 1] = mappings[i][j] + [(i, j)]
            else:
                mappings[i + 1][j + 1] = max(mappings[i + 1][j], mappings[i][j + 1], key=len)
    return find_best_solution(mappings)


def find_best_solution(matrix):
    max_value = 0
    separateness_of_best_solution = float("inf")
    max_index = 0, 0

    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if len(matrix[i][j]) >= max_value:
                separateness = calculate_separatedness(matrix[i][j])
                if len(matrix[i][j]) == max_value:
                    if separateness >= separateness_of_best_solution:
                        continue
                max_value = len(matrix[i][j])
                max_index = (i, j)
                separateness_of_best_solution = separateness

    return matrix[max_index[0]][max_index[1]]


def calculate_separatedness(mapped_indexes):
    if not mapped_indexes:
        return 0
    first_str_indexes, second_str_indexes = zip(*mapped_indexes)
    return sum(
        first_str_indexes[i+1] - first_str_indexes[i] for i in range(len(first_str_indexes) - 1)
    ) + sum(
        second_str_indexes[i+1] - second_str_indexes[i] for i in range(len(second_str_indexes) - 1)
    )
