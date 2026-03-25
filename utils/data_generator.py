from __future__ import annotations

import random
from typing import Any


def random_array(size: int, low: int = 1, high: int = 100) -> list[int]:
    return [random.randint(low, high) for _ in range(size)]


def sorted_array(size: int) -> list[int]:
    return list(range(size))


def reversed_array(size: int) -> list[int]:
    return list(range(size - 1, -1, -1))


def nearly_sorted_array(size: int, swaps: int | None = None) -> list[int]:
    arr = list(range(size))
    if size < 2:
        return arr
    k = swaps if swaps is not None else max(1, size // 20)
    k = min(k, size * (size - 1) // 2)
    for _ in range(k):
        i = random.randrange(size)
        j = random.randrange(size)
        arr[i], arr[j] = arr[j], arr[i]
    return arr


def random_graph(
    n_nodes: int,
    n_edges: int,
    weighted: bool = True,
    directed: bool = False,
) -> dict[int, Any]:
    if n_nodes <= 0:
        return {}
    nodes = list(range(n_nodes))
    graph: dict[int, Any] = {i: {} if weighted else [] for i in nodes}
    edge_set: set[tuple[int, int]] = set()
    max_e = n_nodes * (n_nodes - 1)
    if not directed:
        max_e //= 2
    target = min(n_edges, max_e)
    attempts = 0
    while len(edge_set) < target and attempts < target * 50:
        attempts += 1
        u, v = random.sample(nodes, 2)
        if not directed and u > v:
            u, v = v, u
        if (u, v) in edge_set:
            continue
        edge_set.add((u, v))
        w = random.uniform(0.1, 10.0) if weighted else 1.0
        if weighted:
            graph[u][v] = w
            if not directed:
                graph[v][u] = w
        else:
            graph[u].append(v)
            if not directed:
                graph[v].append(u)
    return graph


def complete_graph(n_nodes: int, weighted: bool = True) -> dict[int, Any]:
    graph: dict[int, Any] = {i: {} if weighted else [] for i in range(n_nodes)}
    for u in range(n_nodes):
        for v in range(u + 1, n_nodes):
            w = random.uniform(0.1, 10.0) if weighted else 1.0
            if weighted:
                graph[u][v] = w
                graph[v][u] = w
            else:
                graph[u].append(v)
                graph[v].append(u)
    return graph


def random_points(
    n: int,
    x_range: tuple[float, float] = (0, 100),
    y_range: tuple[float, float] = (0, 100),
) -> list[tuple[float, float]]:
    xa, xb = x_range
    ya, yb = y_range
    return [
        (random.uniform(xa, xb), random.uniform(ya, yb)) for _ in range(n)
    ]
