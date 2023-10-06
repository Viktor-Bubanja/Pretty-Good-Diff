# Pretty Good Diff

This tool allows developers to compare two objects and see a highlight of the differences between them. It works with strings and dictionaries.
This project was made to help me fix unit tests with failing assertions quicker, especially when the objects are huge or very nested and complicated.
I simply call `show_diff` on the two objects before an assert statement.

## show_diff
Import the `show_diff` method like `from pretty_good_diff import show_diff`.

Then, call `show_diff(first_object, second_object)` to see a colored diff of the input objects. `first_object` and `second_object` need to have the same type and be either `str` or `dict` objects.

Before:
![alt text](https://github.com/Viktor-Bubanja/pretty-good-diff/raw/main/blob/ugly_diff.png)

After:
![alt text](https://github.com/Viktor-Bubanja/pretty-good-diff/raw/main/blob/pretty_good_diff.png)
