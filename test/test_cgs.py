"""
Test: pycgs.cgs
"""


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
        {"relationships": [], "primary_term_dict": {}},
    ]
    for test in tests:
        assert foundational_cgs(test["relationships"]) == test["primary_term_dict"]


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
