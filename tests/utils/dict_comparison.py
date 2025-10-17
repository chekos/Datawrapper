"""Utilities for comparing dictionary structures and values."""

from typing import Any


def extract_field_paths(obj: dict[str, Any], prefix: str = "") -> set[str]:
    """
    Extract all field paths from a nested dictionary.

    Args:
        obj: Dictionary to extract paths from
        prefix: Current path prefix

    Returns:
        Set of all field paths in dot notation

    Example:
        >>> extract_field_paths({"a": {"b": 1, "c": 2}, "d": 3})
        {'a', 'a.b', 'a.c', 'd'}
    """
    paths = set()
    for key, value in obj.items():
        current_path = f"{prefix}.{key}" if prefix else key
        paths.add(current_path)
        if isinstance(value, dict):
            paths.update(extract_field_paths(value, current_path))
    return paths


def compare_dict_structures(
    actual: dict[str, Any], expected: dict[str, Any], path: str = ""
) -> list[str]:
    """
    Compare two dictionary structures and return list of structural differences.

    Args:
        actual: The actual dictionary
        expected: The expected dictionary
        path: Current path for nested comparison

    Returns:
        List of difference descriptions
    """
    differences = []

    # Check for missing keys in actual
    for key in expected:
        if key not in actual:
            full_path = f"{path}.{key}" if path else key
            differences.append(f"Missing key: {full_path}")

    # Check for extra keys in actual
    for key in actual:
        if key not in expected:
            full_path = f"{path}.{key}" if path else key
            differences.append(f"Extra key: {full_path}")

    # Recursively check nested dictionaries
    for key in expected:
        if key in actual:
            full_path = f"{path}.{key}" if path else key
            expected_val = expected[key]
            actual_val = actual[key]

            # If both are dicts, recurse
            if isinstance(expected_val, dict) and isinstance(actual_val, dict):
                differences.extend(
                    compare_dict_structures(actual_val, expected_val, full_path)
                )
            # If types don't match, note the difference
            elif type(expected_val) is not type(actual_val):
                differences.append(
                    f"Type mismatch at {full_path}: "
                    f"expected {type(expected_val).__name__}, "
                    f"got {type(actual_val).__name__}"
                )

    return differences


def compare_dict_values(
    actual: dict[str, Any],
    expected: dict[str, Any],
    path: str = "",
    ignore_missing: bool = False,
) -> list[dict[str, Any]]:
    """
    Compare dictionary values and return detailed comparison results.

    Args:
        actual: The actual dictionary
        expected: The expected dictionary
        path: Current path for nested comparison
        ignore_missing: If True, don't report missing keys as mismatches

    Returns:
        List of comparison results with keys: path, status, expected, actual, message
    """
    results = []

    # Check all keys in expected
    for key in expected:
        full_path = f"{path}.{key}" if path else key
        expected_val = expected[key]

        if key not in actual:
            if not ignore_missing:
                results.append(
                    {
                        "path": full_path,
                        "status": "missing",
                        "expected": expected_val,
                        "actual": None,
                        "message": f"Missing key: {full_path}",
                    }
                )
        else:
            actual_val = actual[key]

            # If both are dicts, recurse
            if isinstance(expected_val, dict) and isinstance(actual_val, dict):
                results.extend(
                    compare_dict_values(
                        actual_val, expected_val, full_path, ignore_missing
                    )
                )
            else:
                # Compare values
                if expected_val == actual_val:
                    results.append(
                        {
                            "path": full_path,
                            "status": "match",
                            "expected": expected_val,
                            "actual": actual_val,
                            "message": f"✓ {full_path}: values match",
                        }
                    )
                else:
                    results.append(
                        {
                            "path": full_path,
                            "status": "mismatch",
                            "expected": expected_val,
                            "actual": actual_val,
                            "message": f"✗ {full_path}: expected {expected_val}, got {actual_val}",
                        }
                    )

    # Check for extra keys in actual
    for key in actual:
        if key not in expected:
            full_path = f"{path}.{key}" if path else key
            results.append(
                {
                    "path": full_path,
                    "status": "extra",
                    "expected": None,
                    "actual": actual[key],
                    "message": f"Extra key: {full_path}",
                }
            )

    return results


def summarize_comparison(results: list[dict[str, Any]]) -> dict[str, Any]:
    """
    Summarize comparison results into counts and categories.

    Args:
        results: List of comparison results from compare_dict_values

    Returns:
        Summary dictionary with counts and categorized results
    """
    summary: dict[str, Any] = {
        "total": len(results),
        "matches": 0,
        "mismatches": 0,
        "missing": 0,
        "extra": 0,
        "match_rate": 0.0,
        "by_status": {"match": [], "mismatch": [], "missing": [], "extra": []},
    }

    for result in results:
        status = result["status"]
        # Handle pluralization for count keys
        if status == "match":
            summary["matches"] = summary["matches"] + 1
        elif status == "mismatch":
            summary["mismatches"] = summary["mismatches"] + 1
        elif status == "missing":
            summary["missing"] = summary["missing"] + 1
        elif status == "extra":
            summary["extra"] = summary["extra"] + 1

        summary["by_status"][status].append(result)

    # Calculate match rate (excluding missing/extra)
    matches = summary["matches"]
    mismatches = summary["mismatches"]
    comparable = matches + mismatches
    if comparable > 0:
        summary["match_rate"] = matches / comparable

    return summary


def print_comparison_summary(
    results: list[dict[str, Any]], title: str = "Comparison Summary"
):
    """
    Print a formatted summary of comparison results.

    Args:
        results: List of comparison results from compare_dict_values
        title: Title for the summary
    """
    summary = summarize_comparison(results)

    print(f"\n{title}")
    print("=" * len(title))
    print(f"Total fields: {summary['total']}")
    print(f"Matches: {summary['matches']} ({summary['match_rate']:.1%})")
    print(f"Mismatches: {summary['mismatches']}")
    print(f"Missing: {summary['missing']}")
    print(f"Extra: {summary['extra']}")

    # Print mismatches
    if summary["mismatches"] > 0:
        print(f"\nMismatches ({summary['mismatches']}):")
        for result in summary["by_status"]["mismatch"]:
            print(f"  {result['message']}")

    # Print missing
    if summary["missing"] > 0:
        print(f"\nMissing ({summary['missing']}):")
        for result in summary["by_status"]["missing"]:
            print(f"  {result['message']}")

    # Print extra
    if summary["extra"] > 0:
        print(f"\nExtra ({summary['extra']}):")
        for result in summary["by_status"]["extra"]:
            print(f"  {result['message']}")


def find_type_mismatches(
    actual: dict[str, Any], expected: dict[str, Any]
) -> list[dict[str, str]]:
    """
    Find fields where the data types don't match between dictionaries.

    Args:
        actual: The actual dictionary
        expected: The expected dictionary

    Returns:
        List of type mismatch information
    """
    mismatches = []

    def _check_types(act_dict, exp_dict, path=""):
        for key in exp_dict:
            if key in act_dict:
                full_path = f"{path}.{key}" if path else key
                exp_val = exp_dict[key]
                act_val = act_dict[key]

                if type(exp_val) is not type(act_val):
                    mismatches.append(
                        {
                            "path": full_path,
                            "expected_type": type(exp_val).__name__,
                            "actual_type": type(act_val).__name__,
                            "expected_value": str(exp_val),
                            "actual_value": str(act_val),
                        }
                    )
                elif isinstance(exp_val, dict) and isinstance(act_val, dict):
                    _check_types(act_val, exp_val, full_path)

    _check_types(actual, expected)
    return mismatches


def get_field_coverage(
    actual: dict[str, Any], expected: dict[str, Any]
) -> dict[str, int | float | set[str]]:
    """
    Calculate field coverage statistics between two dictionaries.

    Args:
        actual: The actual dictionary
        expected: The expected dictionary

    Returns:
        Coverage statistics including counts and field sets
    """
    actual_fields = extract_field_paths(actual)
    expected_fields = extract_field_paths(expected)

    supported = actual_fields & expected_fields
    missing = expected_fields - actual_fields
    extra = actual_fields - expected_fields

    coverage_rate = len(supported) / len(expected_fields) if expected_fields else 0.0

    return {
        "total_expected": len(expected_fields),
        "total_actual": len(actual_fields),
        "supported": len(supported),
        "missing": len(missing),
        "extra": len(extra),
        "coverage_rate": coverage_rate,
        "supported_fields": supported,
        "missing_fields": missing,
        "extra_fields": extra,
    }
