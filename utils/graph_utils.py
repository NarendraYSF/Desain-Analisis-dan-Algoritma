from __future__ import annotations

import math
from typing import Any

import networkx as nx


def adj_list_to_matrix(graph: dict[int, Any], n: int) -> list[list[float]]:
    inf = float("inf")
    mat = [[inf] * n for _ in range(n)]
    for i in range(n):
        mat[i][i] = 0.0
    for u, nbrs in graph.items():
        if u < 0 or u >= n:
            continue
        if isinstance(nbrs, dict):
            for v, w in nbrs.items():
                if 0 <= v < n:
                    mat[u][v] = float(w)
        else:
            for v in nbrs:
                if 0 <= v < n:
                    mat[u][v] = 1.0
    return mat


def matrix_to_adj_list(matrix: list[list[float]]) -> dict[int, dict[int, float]]:
    n = len(matrix)
    graph: dict[int, dict[int, float]] = {i: {} for i in range(n)}
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            w = matrix[i][j]
            if w != float("inf") and not math.isnan(w):
                graph[i][j] = float(w)
    return graph


def _all_nodes(graph: dict[Any, Any]) -> list[Any]:
    s: set[Any] = set(graph.keys())
    for u, nbrs in graph.items():
        if isinstance(nbrs, dict):
            s.update(nbrs.keys())
        else:
            s.update(nbrs)
    return sorted(s, key=lambda x: (isinstance(x, str), x))


def get_layout(graph: dict[Any, Any]) -> dict[Any, tuple[float, float]]:
    nodes = _all_nodes(graph)
    if not nodes:
        return {}
    n = len(nodes)
    idx = {node: k for k, node in enumerate(nodes)}
    edges: list[tuple[int, int]] = []
    for u, nbrs in graph.items():
        ui = idx.get(u)
        if ui is None:
            continue
        if isinstance(nbrs, dict):
            for v in nbrs:
                vi = idx.get(v)
                if vi is not None and ui != vi:
                    edges.append((ui, vi))
        else:
            for v in nbrs:
                vi = idx.get(v)
                if vi is not None and ui != vi:
                    edges.append((ui, vi))

    radius = max(2.0, n / (2 * math.pi))
    pos: list[tuple[float, float]] = []
    for k in range(n):
        ang = 2 * math.pi * k / max(n, 1)
        pos.append((radius * math.cos(ang), radius * math.sin(ang)))

    k_attr = 0.1 * radius * radius
    k_rep = 0.01 * radius * radius * radius
    dt = 0.04
    iterations = max(50, 15 * n)

    for _ in range(iterations):
        disp = [(0.0, 0.0) for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                dx = pos[i][0] - pos[j][0]
                dy = pos[i][1] - pos[j][1]
                dist = math.hypot(dx, dy) + 1e-6
                force = k_rep / (dist * dist)
                fx = force * dx / dist
                fy = force * dy / dist
                di = disp[i]
                dj = disp[j]
                disp[i] = (di[0] + fx, di[1] + fy)
                disp[j] = (dj[0] - fx, dj[1] - fy)
        for i, j in edges:
            dx = pos[j][0] - pos[i][0]
            dy = pos[j][1] - pos[i][1]
            dist = math.hypot(dx, dy) + 1e-6
            force = k_attr * dist
            fx = force * dx / dist
            fy = force * dy / dist
            di = disp[i]
            dj = disp[j]
            disp[i] = (di[0] + fx, di[1] + fy)
            disp[j] = (dj[0] - fx, dj[1] - fy)
        for i in range(n):
            dx, dy = disp[i]
            mag = math.hypot(dx, dy) + 1e-9
            cap = 0.5 * radius
            if mag > cap:
                dx, dy = dx * cap / mag, dy * cap / mag
            pos[i] = (pos[i][0] + dx * dt, pos[i][1] + dy * dt)

    return {nodes[i]: pos[i] for i in range(n)}


def _is_directed_adjacency(graph: dict[Any, Any]) -> bool:
    for u, nbrs in graph.items():
        if isinstance(nbrs, dict):
            for v in nbrs:
                back = graph.get(v)
                if not isinstance(back, dict) or u not in back:
                    return True
        else:
            for v in nbrs:
                back = graph.get(v, [])
                if isinstance(back, dict):
                    return True
                if u not in back:
                    return True
    return False


def graph_to_networkx(graph: dict[Any, Any]) -> Any:
    directed = _is_directed_adjacency(graph)
    G: nx.Graph | nx.DiGraph = nx.DiGraph() if directed else nx.Graph()
    for u, nbrs in graph.items():
        G.add_node(u)
        if isinstance(nbrs, dict):
            for v, w in nbrs.items():
                G.add_node(v)
                G.add_edge(u, v, weight=float(w))
        else:
            for v in nbrs:
                G.add_node(v)
                G.add_edge(u, v)
    return G
