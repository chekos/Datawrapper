"""Test utilities package."""

import json

import pandas as pd
from pydantic import BaseModel

from .dict_comparison import (
    compare_dict_structures,
    compare_dict_values,
    extract_field_paths,
    find_type_mismatches,
    get_field_coverage,
    print_comparison_summary,
    summarize_comparison,
)

__all__ = [
    "compare_dict_structures",
    "compare_dict_values",
    "extract_field_paths",
    "find_type_mismatches",
    "get_field_coverage",
    "print_comparison_summary",
    "summarize_comparison",
    "_test_class",
]


class PydanticJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, BaseModel):
            return obj.model_dump(by_alias=True)
        elif isinstance(obj, pd.DataFrame):
            return obj.to_dict(orient="records")
        return super().default(obj)


def _test_class(cls):
    """Test a class by validating an example, dumping it to JSON, and then validating again."""
    example_list = cls.model_config.get("json_schema_extra", {}).get("examples")
    assert len(example_list) > 0

    for example in example_list:
        # Validate it
        cls.model_validate(example)

        # Create an object
        obj = cls(**example)

        # Dump it to Python
        assert obj.model_dump(by_alias=True)

        # Dump it to JSON
        input_json = json.dumps(example, cls=PydanticJSONEncoder)

        # Deserialize from JSON to Python
        obj = cls.model_validate_json(input_json)

        # Dump that to Python
        assert obj.model_dump(by_alias=True)

        # Serialize from Python to JSON
        obj.model_dump_json(by_alias=True)
