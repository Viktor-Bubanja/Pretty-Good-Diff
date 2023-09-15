import setuptools

with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "pretty-good-diff",
    version = "0.0.1",
    author = "Viktor Bubanja",
    author_email = "viktor.bubanja@hotmail.com",
    description = "Gives you a pretty good diff between two objects",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/Viktor-Bubanja/pretty-good-diff",
    keywords= ["diff", "difference", "checker", "highlight", "color", "colour", "colored", "coloured"],
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir = {"": "src"},
    packages = setuptools.find_packages(where="src"),
    python_requires = ">=3.9"
)
