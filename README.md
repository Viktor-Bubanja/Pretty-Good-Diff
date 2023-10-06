# Pretty Good Diff

This tool allows developers to compare two objects and see a highlight of the differences between them. It works with strings and dictionaries.
This project was made to help me fix unit tests with failing assertions quicker, especially when the objects are huge or very nested and complicated.
I simply call `show_diff` on the two objects before an assert statement (note: if you're running this within Pytest, you need to pass a `-s` flag to your Pytest command to [disable output capturing](https://docs.pytest.org/en/7.1.x/how-to/capture-stdout-stderr.html) and see the output of print statements).

**How to use**

Import the `show_diff` method like `from pretty_good_diff import show_diff`.

Then, call `show_diff(first_object, second_object)` to see a colored diff of the input objects. `first_object` and `second_object` need to have the same type and be either `str` or `dict` objects.

Before:
![alt text](https://github.com/Viktor-Bubanja/pretty-good-diff/raw/main/blob/ugly_diff.png)

After:
![alt text](https://github.com/Viktor-Bubanja/pretty-good-diff/raw/main/blob/pretty_good_diff.png)

**Solution**

To calculate the difference between two dictionaries, a straightforward algorithm is used which recursively compares nested dictionaries. For key-value pairs where the values are strings, the string-difference algorithm is utilised. The string-difference algorithm implemented here leverages dynamic programming to identify the largest set of common substrings between two strings, prioritising longer sequences over multiple shorter ones. With a time complexity of *O(N x M)*, where *N* and *M* are the lengths of the two input strings, the algorithm remains performant even for larger inputs.
