from src.dictionary import get_diff


def test_get_diff_finds_differences_in_nested_dictionaries():
    sentinel = object()
    dictionary_1 = {"a": 123, "b": {"c": "zzz", "d": "xxx", "e": {"f": None, "g": 6, "h": 5}}, "i": 456, "j": 1}
    dictionary_2 = {"a": 123, "b": {"c": "zzz", "d": "yyy", "e": {"f": 4, "g": 6}}, "i": 789, "k": 2}

    difference = get_diff(dictionary_1, dictionary_2, {}, sentinel)
    expected_difference = {
        "b": {
            "d": ("xxx", "yyy"),
            "e": {
                "f": (None, 4),
                "h": (5, sentinel),
            },
        },
        "i": (456, 789),
        "j": (1, sentinel),
        "k": (sentinel, 2),
    }
    assert difference == expected_difference
