from typing import Optional
from pydantic import BaseModel
from src.pydantic import get_diff


def test_get_diff_finds_differences_in_nested_pydantic_objects():
    sentinel = object()
    class SomeNestedClass(BaseModel):
        c: str
        d: int
        e: Optional[str]

    class SomeClass(BaseModel):
        a: str
        b: SomeNestedClass
    obj_1 = SomeClass(a="abc", b=SomeNestedClass(c="def", d=123, e="xxx"))
    obj_2 = SomeClass(a="tuv", b=SomeNestedClass(c="ghi", d=123))

    difference = get_diff(obj_1, obj_2, {}, sentinel)
    expected_difference = {
        "a": ("abc", "tuv"),
        "b": {
            "c": ("def", "ghi"),
            "e": ("xxx", None)
        }
    }
    assert difference == expected_difference
