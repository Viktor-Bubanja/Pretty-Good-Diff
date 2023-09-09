# Pretty Good Diff

Pretty Good Diff is a tool that allows users to compare two objects and see a highlight of the differences between them. It works with strings, dictionaries, and Pydantic objects.

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
>> first_object = {"a": 1, "b": 2}
>> second_object = {"a": 1, "b": 3}
>> get_diff(first_object, second_object)
{"b": (2, 3)}
```
