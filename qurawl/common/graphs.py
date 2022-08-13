# -*- coding: utf-8 -*-

"""Graph Algorithms
"""

####




####

__all__ = ['dfs']

####

def dfs_connected(graph, start):
    """Depth First Search

    Find nodes in connected subgraph with node 'start'.

    Args:
        graph:
             An instance of dict.
        start:
             A key in graph.

    Returns:
        visited:
            A set of nodes.
    """
    assert isinstance(graph, dict), 'Not a Graph'
    assert start in graph, 'Node not in Graph'

    stack = [start]
    visited = set()
    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            # ask for permission because it can be a defaultdict! (no try, except)
            if node in graph:
                next_nodes = graph[node]
                stack.extend(next_nodes)

    return visited

####
