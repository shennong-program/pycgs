"""
Test: pycgs.cgs
"""

import pytest

from pycgs.cgs import (
    foundational_cgs,
    weighted_cgs,
)


def test_foundational_cgs():
    """
    Test foundational_cgs() function.
    """
    tests = [
        {
            "relationships": [("A", "B"), ("B", "C"), ("D", "B"), ("E", "F")],
            "primary_term_dict": {
                "A": "C",
                "B": "C",
                "C": "C",
                "D": "C",
                "E": "F",
                "F": "F",
            },
        },
        {
            "relationships": [("A", "B"), ("B", "C"), ("C", "D"), ("D", "E")],
            "primary_term_dict": {"A": "E", "B": "E", "C": "E", "D": "E", "E": "E"},
        },
        # Test duplicate relationships
        {
            "relationships": [("A", "B"), ("B", "C"), ("A", "B"), ("B", "C")],
            "primary_term_dict": {"A": "C", "B": "C", "C": "C"},
        },
        # Test empty relationships
        {"relationships": [], "primary_term_dict": {}},
        # Test branch node
        {
            "relationships": [
                ("A", "B"),
                ("B", "D"),  # B is a branch node
                ("B", "C"),
                ("B", "a"),
                ("a", "E"),
            ],
            "primary_term_dict": {
                "A": "C",  # For branch B, its successor nodes' alphabetical order is C, D, a. Thus, A -> C; rather than D or a.
                "B": "C",
                "C": "C",
                "D": "D",
                "E": "E",
                "a": "E",
            },
        },
    ]
    for test in tests:
        assert foundational_cgs(test["relationships"]) == test["primary_term_dict"]

    value_error_tests = [
        {
            # The graph is not a Directed Acyclic Graph
            "relationships": [("A", "B"), ("B", "C"), ("C", "A")],
        },
    ]
    for test in value_error_tests:
        with pytest.raises(ValueError):
            foundational_cgs(test["relationships"])


def test_weighted_cgs():
    """
    Test weighted_cgs() function.
    """
    tests = [
        {
            "relationships": [
                ("A", "B", 1),
                ("B", "C", 2),
                ("D", "B", 1),
                ("B", "E", 1),
            ],
            "primary_term_dict": {"A": "C", "B": "C", "C": "C", "D": "C", "E": "E"},
        },
    ]
    for test in tests:
        assert weighted_cgs(test["relationships"]) == test["primary_term_dict"]
