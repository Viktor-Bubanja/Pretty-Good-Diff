import json
from typing import Optional
from src.dictionary import get_diff as get_dict_diff

def get_diff(first_json: str, second_json: str, output_dict: Optional[dict] = None, sentinel = object()) -> dict:
    return get_dict_diff(json.loads(first_json), json.loads(second_json), {}, sentinel)
