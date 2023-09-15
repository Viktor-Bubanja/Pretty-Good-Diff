# Pretty Good Diff

This tool allows developers to compare two objects and see a highlight of the differences between them. It works with strings and dictionaries.
This project was made to help me fix unit tests with failing assertions quicker, especially when the objects are huge or very nested and complicated.
I simply call `show_diff` on the two objects before an assert statement.
It's not outstanding, but it's pretty good.

## show_diff

Just call `show_diff(first_object, second_object)` to see a colored diff of the input objects.

Before:
![alt text](blob/ugly_diff.png?raw=true)

After:
![alt text](blob/pretty_good_diff.png?raw=true)


## get_diff

Alternatively, for comparing dictionaries or Pydantic objects, if you want to have a dictionary containing tuples with the differing values/fields of the first and second object respectively, call `get_diff(first_object, second_object)`.
For example:
```
>> first_object = {
    "a": 123,
    "b": {
        "c": "zzz",
        "d": "xxx",
        "e": {"f": None, "g": 6, "h": 5, "i": "ababc"},
    },
    "i": 456,
    "j": 1,
}
>> second_object = {
    "a": 123,
    "b": {"c": "zzz", "d": "yyy", "e": {"f": 4, "g": 6, "i": "abcde"}},
    "i": 789,
    "k": 2,
}
>> get_diff(first_object, second_object)
{
    "b": {
        "d": [],
        "e": {
            "f": (None, 4),
            "h": (5, sentinel),
            "i": [(2, 0), (3, 1), (4, 2)],
        },
    },
    "i": (456, 789),
    "j": (1, sentinel),
    "k": (sentinel, 2),
}
```
(string diffs are represented as lists of tuples that map the indices of matching characters between strings)
