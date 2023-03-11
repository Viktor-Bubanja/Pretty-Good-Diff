from typing import Optional
from pydantic import BaseModel
from src.dictionary import get_diff as get_dict_diff


def get_diff(first_obj: BaseModel, second_obj: BaseModel, output_dict: Optional[dict] = None, sentinel = None) -> dict:
    return get_dict_diff(first_obj.dict(), second_obj.dict())
