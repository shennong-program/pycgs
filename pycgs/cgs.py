"""
This module contains the algorithms for Coreference-based Graph Search (CGS).
"""

import networkx as nx

from pycgs.type import Edge, EdgeWithWeight


__all__ = ["foundational_cgs", "weighted_cgs"]


def foundational_cgs(relationships: list[Edge]) -> dict[str, str]:
    """
    Foundational CGS algorithm.
    """
    # Create a Directed Acyclic Graph
    cptg = nx.DiGraph()  # CPTG: Coreference-based Primary Term Graph

    # Add edges to the graph based on the coreference relationships
    cptg.add_edges_from(set(relationships))  # Use set to remove duplicates

    # Check if the graph is a Directed Acyclic Graph
    if not nx.is_directed_acyclic_graph(cptg):
        raise ValueError("The graph is  not a Directed Acyclic Graph.")

    # Initialize the dictionary to store the ultimate Primary Terms
    primary_term_dict = {}

    # Iterate through each node in the graph
    for node in cptg.nodes():
        # Check if the node is a Primary Term (out-degree == 0)
        if cptg.out_degree(node) == 0:
            # The node is a Primary Term, map it to itself
            primary_term_dict[node] = node
        else:
            # The node is not a Primary Term, find its ultimate Primary Term
            current = node
            while cptg.out_degree(current) != 0:
                # Follow the directed edges to find the Primary Term
                current = sorted(cptg.successors(current))[
                    0
                ]  # Sort to get a deterministic result
            primary_term_dict[node] = current

    return primary_term_dict


def weighted_cgs(relationships: list[EdgeWithWeight]) -> dict[str, str]:
    """
    Weighted CGS algorithm.
    """
    # Create a Directed Acyclic Graph
    cptg = nx.DiGraph()  # CPTG: Coreference-based Primary Term Graph

    # Add weighted edges to the graph based on the coreference relationships
    for src, tgt, weight in relationships:
        cptg.add_edge(src, tgt, weight=weight)

    # Initialize the dictionary to store the ultimate Primary Terms
    primary_term_dict = {}

    # Iterate through each node in the graph
    for node in cptg.nodes():
        # Check if the node is a Primary Term (out-degree == 0)
        if cptg.out_degree(node) == 0:
            primary_term_dict[node] = node
        else:
            # The node is not a Primary Term, find its ultimate Primary Term
            current_node = node
            while cptg.out_degree(current_node) != 0:
                # Get the downstream node with the highest weight
                successors = list(cptg.successors(current_node))
                if successors:
                    highest_weight_edge = max(
                        successors,
                        key=lambda succ, current=current_node: cptg[current][succ][
                            "weight"
                        ],
                    )
                    current_node = highest_weight_edge
                else:
                    break
            primary_term_dict[node] = current_node

    return primary_term_dict
