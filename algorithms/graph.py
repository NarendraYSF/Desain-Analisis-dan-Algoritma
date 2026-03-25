from __future__ import annotations

import heapq
from collections import deque
from typing import Any, Callable, Dict, Generator, List, Optional, Set, Tuple, TypedDict

Graph = Dict[int, List[Tuple[int, float]]]


class AlgoMeta(TypedDict):
    traced: Callable[..., Any]
    plain: Callable[..., Any]
    time: str
    space: str
    description: str


def _all_vertices(graph: Graph) -> Set[int]:
    vs: Set[int] = set(graph.keys())
    for nbrs in graph.values():
        for v, _ in nbrs:
            vs.add(v)
    return vs


def _undirected_edges(graph: Graph) -> List[Tuple[int, int, float]]:
    best: Dict[Tuple[int, int], float] = {}
    for u, nbrs in graph.items():
        for v, w in nbrs:
            a, b = (u, v) if u <= v else (v, u)
            t = (a, b)
            if t not in best or w < best[t]:
                best[t] = w
    return [(a, b, best[(a, b)]) for a, b in sorted(best.keys())]


def bfs_traced(
    graph: Graph, start: int
) -> Generator[Dict[str, Any], None, None]:
    visited: Set[int] = set()
    queue: deque[int] = deque([start])
    parent: Dict[int, Optional[int]] = {start: None}
    edges_explored: List[Tuple[int, int]] = []
    step = 0
    visited.add(start)
    yield {
        "visited": set(visited),
        "queue": list(queue),
        "current": start,
        "parent": dict(parent),
        "step": step,
        "edges_explored": list(edges_explored),
    }
    step += 1
    while queue:
        u = queue.popleft()
        yield {
            "visited": set(visited),
            "queue": list(queue),
            "current": u,
            "parent": dict(parent),
            "step": step,
            "edges_explored": list(edges_explored),
        }
        step += 1
        for v, _ in graph.get(u, []):
            edges_explored.append((u, v))
            yield {
                "visited": set(visited),
                "queue": list(queue),
                "current": u,
                "parent": dict(parent),
                "step": step,
                "edges_explored": list(edges_explored),
            }
            step += 1
            if v not in visited:
                visited.add(v)
                parent[v] = u
                queue.append(v)
                yield {
                    "visited": set(visited),
                    "queue": list(queue),
                    "current": u,
                    "parent": dict(parent),
                    "step": step,
                    "edges_explored": list(edges_explored),
                }
                step += 1


def bfs(graph: Graph, start: int) -> Tuple[List[int], Dict[int, Optional[int]]]:
    order: List[int] = []
    parent: Dict[int, Optional[int]] = {start: None}
    visited: Set[int] = set()
    q: deque[int] = deque([start])
    visited.add(start)
    while q:
        u = q.popleft()
        order.append(u)
        for v, _ in graph.get(u, []):
            if v not in visited:
                visited.add(v)
                parent[v] = u
                q.append(v)
    return order, parent


def dfs_traced(
    graph: Graph, start: int
) -> Generator[Dict[str, Any], None, None]:
    visited: Set[int] = set()
    stack: List[int] = [start]
    parent: Dict[int, Optional[int]] = {start: None}
    edges_explored: List[Tuple[int, int]] = []
    step = 0
    yield {
        "visited": set(visited),
        "stack": list(stack),
        "current": start,
        "parent": dict(parent),
        "step": step,
        "edges_explored": list(edges_explored),
    }
    step += 1
    while stack:
        u = stack.pop()
        if u in visited:
            yield {
                "visited": set(visited),
                "stack": list(stack),
                "current": u,
                "parent": dict(parent),
                "step": step,
                "edges_explored": list(edges_explored),
            }
            step += 1
            continue
        visited.add(u)
        yield {
            "visited": set(visited),
            "stack": list(stack),
            "current": u,
            "parent": dict(parent),
            "step": step,
            "edges_explored": list(edges_explored),
        }
        step += 1
        nbrs = list(graph.get(u, []))
        for v, _ in reversed(nbrs):
            edges_explored.append((u, v))
            yield {
                "visited": set(visited),
                "stack": list(stack),
                "current": u,
                "parent": dict(parent),
                "step": step,
                "edges_explored": list(edges_explored),
            }
            step += 1
            if v not in visited:
                parent[v] = u
                stack.append(v)
                yield {
                    "visited": set(visited),
                    "stack": list(stack),
                    "current": u,
                    "parent": dict(parent),
                    "step": step,
                    "edges_explored": list(edges_explored),
                }
                step += 1


def dfs(graph: Graph, start: int) -> Tuple[List[int], Dict[int, Optional[int]]]:
    order: List[int] = []
    parent: Dict[int, Optional[int]] = {start: None}
    visited: Set[int] = set()
    stack: List[int] = [start]
    while stack:
        u = stack.pop()
        if u in visited:
            continue
        visited.add(u)
        order.append(u)
        for v, _ in reversed(graph.get(u, [])):
            if v not in visited:
                parent[v] = u
                stack.append(v)
    return order, parent


def dijkstra_traced(
    graph: Graph, start: int
) -> Generator[Dict[str, Any], None, None]:
    vertices = _all_vertices(graph)
    inf = float("inf")
    distances: Dict[int, float] = {v: inf for v in vertices}
    distances[start] = 0.0
    visited: Set[int] = set()
    heap: List[Tuple[float, int]] = [(0.0, start)]
    step = 0
    yield {
        "distances": dict(distances),
        "visited": set(visited),
        "current": start,
        "relaxed_edge": (start, start),
        "step": step,
    }
    step += 1
    while heap:
        d_u, u = heapq.heappop(heap)
        if u in visited:
            continue
        if d_u != distances[u]:
            continue
        visited.add(u)
        yield {
            "distances": dict(distances),
            "visited": set(visited),
            "current": u,
            "relaxed_edge": (u, u),
            "step": step,
        }
        step += 1
        for v, w in graph.get(u, []):
            yield {
                "distances": dict(distances),
                "visited": set(visited),
                "current": u,
                "relaxed_edge": (u, v),
                "step": step,
            }
            step += 1
            nd = d_u + w
            if nd < distances[v]:
                distances[v] = nd
                heapq.heappush(heap, (nd, v))
                yield {
                    "distances": dict(distances),
                    "visited": set(visited),
                    "current": u,
                    "relaxed_edge": (u, v),
                    "step": step,
                }
                step += 1


def dijkstra(
    graph: Graph, start: int
) -> Dict[int, float]:
    vertices = _all_vertices(graph)
    inf = float("inf")
    dist: Dict[int, float] = {v: inf for v in vertices}
    dist[start] = 0.0
    heap: List[Tuple[float, int]] = [(0.0, start)]
    visited: Set[int] = set()
    while heap:
        d_u, u = heapq.heappop(heap)
        if u in visited:
            continue
        if d_u != dist[u]:
            continue
        visited.add(u)
        for v, w in graph.get(u, []):
            nd = d_u + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(heap, (nd, v))
    return dist


def bellman_ford_traced(
    graph: Graph, start: int
) -> Generator[Dict[str, Any], None, None]:
    vertices = sorted(_all_vertices(graph))
    inf = float("inf")
    distances: Dict[int, float] = {v: inf for v in vertices}
    distances[start] = 0.0
    edges: List[Tuple[int, int, float]] = []
    for u, nbrs in graph.items():
        for v, w in nbrs:
            edges.append((u, v, w))
    step = 0
    n = len(vertices)
    yield {
        "distances": dict(distances),
        "visited": {v for v in vertices if distances[v] < inf},
        "current": start,
        "relaxed_edge": (start, start),
        "step": step,
    }
    step += 1
    for _ in range(max(0, n - 1)):
        for u, v, w in edges:
            yield {
                "distances": dict(distances),
                "visited": {x for x in vertices if distances[x] < inf},
                "current": u,
                "relaxed_edge": (u, v),
                "step": step,
            }
            step += 1
            if distances[u] + w < distances[v]:
                distances[v] = distances[u] + w
                yield {
                    "distances": dict(distances),
                    "visited": {x for x in vertices if distances[x] < inf},
                    "current": u,
                    "relaxed_edge": (u, v),
                    "step": step,
                }
                step += 1
    for u, v, w in edges:
        yield {
            "distances": dict(distances),
            "visited": {x for x in vertices if distances[x] < inf},
            "current": u,
            "relaxed_edge": (u, v),
            "step": step,
        }
        step += 1
        if distances[u] + w < distances[v]:
            distances[v] = distances[u] + w
            yield {
                "distances": dict(distances),
                "visited": {x for x in vertices if distances[x] < inf},
                "current": u,
                "relaxed_edge": (u, v),
                "step": step,
            }
            step += 1


def bellman_ford(
    graph: Graph, start: int
) -> Optional[Dict[int, float]]:
    vertices = list(_all_vertices(graph))
    inf = float("inf")
    dist: Dict[int, float] = {v: inf for v in vertices}
    dist[start] = 0.0
    edges: List[Tuple[int, int, float]] = []
    for u, nbrs in graph.items():
        for v, w in nbrs:
            edges.append((u, v, w))
    n = len(vertices)
    for _ in range(max(0, n - 1)):
        for u, v, w in edges:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
    for u, v, w in edges:
        if dist[u] + w < dist[v]:
            return None
    return dist


class _UnionFind:
    def __init__(self, n: int) -> None:
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x: int) -> int:
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a: int, b: int) -> bool:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.rank[ra] < self.rank[rb]:
            self.parent[ra] = rb
        elif self.rank[ra] > self.rank[rb]:
            self.parent[rb] = ra
        else:
            self.parent[rb] = ra
            self.rank[ra] += 1
        return True


def prim_traced(graph: Graph) -> Generator[Dict[str, Any], None, None]:
    vertices = sorted(_all_vertices(graph))
    vset = set(vertices)
    if not vertices:
        yield {
            "mst_edges": [],
            "total_weight": 0.0,
            "current_edge": (-1, -1, 0.0),
            "step": 0,
        }
        return
    in_tree: Set[int] = set()
    mst_edges: List[Tuple[int, int, float]] = []
    total_weight = 0.0
    step = 0
    heap: List[Tuple[float, int, int]] = []
    for seed in vertices:
        if seed in in_tree:
            continue
        in_tree.add(seed)
        yield {
            "mst_edges": list(mst_edges),
            "total_weight": total_weight,
            "current_edge": (seed, seed, 0.0),
            "step": step,
        }
        step += 1
        for v, w in graph.get(seed, []):
            if v in vset:
                heapq.heappush(heap, (w, seed, v))
        while heap:
            wgt, u, v = heapq.heappop(heap)
            if v in in_tree:
                yield {
                    "mst_edges": list(mst_edges),
                    "total_weight": total_weight,
                    "current_edge": (u, v, wgt),
                    "step": step,
                }
                step += 1
                continue
            yield {
                "mst_edges": list(mst_edges),
                "total_weight": total_weight,
                "current_edge": (u, v, wgt),
                "step": step,
            }
            step += 1
            in_tree.add(v)
            a, b = (u, v) if u <= v else (v, u)
            mst_edges.append((a, b, wgt))
            total_weight += wgt
            yield {
                "mst_edges": list(mst_edges),
                "total_weight": total_weight,
                "current_edge": (u, v, wgt),
                "step": step,
            }
            step += 1
            for x, wx in graph.get(v, []):
                if x not in in_tree and x in vset:
                    heapq.heappush(heap, (wx, v, x))


def prim(graph: Graph) -> Tuple[List[Tuple[int, int, float]], float]:
    vertices = sorted(_all_vertices(graph))
    vset = set(vertices)
    if not vertices:
        return [], 0.0
    in_tree: Set[int] = set()
    mst_edges: List[Tuple[int, int, float]] = []
    total_weight = 0.0
    heap: List[Tuple[float, int, int]] = []
    for seed in vertices:
        if seed in in_tree:
            continue
        in_tree.add(seed)
        for v, w in graph.get(seed, []):
            if v in vset:
                heapq.heappush(heap, (w, seed, v))
        while heap:
            wgt, u, v = heapq.heappop(heap)
            if v in in_tree:
                continue
            in_tree.add(v)
            a, b = (u, v) if u <= v else (v, u)
            mst_edges.append((a, b, wgt))
            total_weight += wgt
            for x, wx in graph.get(v, []):
                if x not in in_tree and x in vset:
                    heapq.heappush(heap, (wx, v, x))
    return mst_edges, total_weight


def kruskal_traced(graph: Graph) -> Generator[Dict[str, Any], None, None]:
    edges = sorted(_undirected_edges(graph), key=lambda e: e[2])
    vertices = sorted(_all_vertices(graph))
    if not vertices:
        yield {
            "mst_edges": [],
            "total_weight": 0.0,
            "current_edge": (-1, -1, 0.0),
            "step": 0,
        }
        return
    idx: Dict[int, int] = {v: i for i, v in enumerate(vertices)}
    uf = _UnionFind(len(vertices))
    mst_edges: List[Tuple[int, int, float]] = []
    total_weight = 0.0
    step = 0
    yield {
        "mst_edges": list(mst_edges),
        "total_weight": total_weight,
        "current_edge": (-1, -1, 0.0),
        "step": step,
    }
    step += 1
    for a, b, w in edges:
        yield {
            "mst_edges": list(mst_edges),
            "total_weight": total_weight,
            "current_edge": (a, b, w),
            "step": step,
        }
        step += 1
        ia, ib = idx[a], idx[b]
        if uf.union(ia, ib):
            mst_edges.append((a, b, w))
            total_weight += w
            yield {
                "mst_edges": list(mst_edges),
                "total_weight": total_weight,
                "current_edge": (a, b, w),
                "step": step,
            }
            step += 1


def kruskal(graph: Graph) -> Tuple[List[Tuple[int, int, float]], float]:
    edges = sorted(_undirected_edges(graph), key=lambda e: e[2])
    vertices = sorted(_all_vertices(graph))
    if not vertices:
        return [], 0.0
    idx: Dict[int, int] = {v: i for i, v in enumerate(vertices)}
    uf = _UnionFind(len(vertices))
    mst: List[Tuple[int, int, float]] = []
    tw = 0.0
    for a, b, w in edges:
        if uf.union(idx[a], idx[b]):
            mst.append((a, b, w))
            tw += w
    return mst, tw


def topological_sort_traced(
    graph: Graph
) -> Generator[Dict[str, Any], None, None]:
    vertices = sorted(_all_vertices(graph))
    visited: Set[int] = set()
    stack: List[int] = []
    order: List[int] = []
    step = 0
    temp: Set[int] = set()
    cycle = [False]

    def dfs(u: int) -> None:
        nonlocal step
        stack.append(u)
        yield {
            "visited": set(visited),
            "stack": list(stack),
            "current": u,
            "order": list(order),
            "step": step,
        }
        step += 1
        temp.add(u)
        for v, _ in graph.get(u, []):
            if v in visited:
                continue
            if v in temp:
                cycle[0] = True
                yield {
                    "visited": set(visited),
                    "stack": list(stack),
                    "current": v,
                    "order": list(order),
                    "step": step,
                }
                step += 1
                return
            yield from dfs(v)
            if cycle[0]:
                return
        temp.remove(u)
        visited.add(u)
        stack.pop()
        order.append(u)
        yield {
            "visited": set(visited),
            "stack": list(stack),
            "current": u,
            "order": list(order),
            "step": step,
        }
        step += 1

    for s in vertices:
        if s not in visited and s not in temp:
            yield from dfs(s)
            if cycle[0]:
                return


def topological_sort(graph: Graph) -> List[int]:
    vertices = sorted(_all_vertices(graph))
    visited: Set[int] = set()
    order: List[int] = []
    temp: Set[int] = set()

    def visit(u: int) -> bool:
        if u in temp:
            return False
        if u in visited:
            return True
        temp.add(u)
        for v, _ in graph.get(u, []):
            if not visit(v):
                return False
        temp.remove(u)
        visited.add(u)
        order.append(u)
        return True

    for s in vertices:
        if s not in visited:
            if not visit(s):
                return []
    return list(reversed(order))


ALGORITHMS: Dict[str, AlgoMeta] = {
    "bfs": {
        "traced": bfs_traced,
        "plain": bfs,
        "time": "O(V + E)",
        "space": "O(V)",
        "description": "Breadth-first traversal from a source; unweighted shortest paths in edges.",
    },
    "dfs": {
        "traced": dfs_traced,
        "plain": dfs,
        "time": "O(V + E)",
        "space": "O(V)",
        "description": "Depth-first traversal from a source using an explicit stack.",
    },
    "dijkstra": {
        "traced": dijkstra_traced,
        "plain": dijkstra,
        "time": "O((V + E) log V)",
        "space": "O(V)",
        "description": "Single-source shortest paths with non-negative edge weights.",
    },
    "bellman_ford": {
        "traced": bellman_ford_traced,
        "plain": bellman_ford,
        "time": "O(V * E)",
        "space": "O(V)",
        "description": "Single-source shortest paths; detects negative cycles (plain returns None).",
    },
    "prim": {
        "traced": prim_traced,
        "plain": prim,
        "time": "O(E log V)",
        "space": "O(V + E)",
        "description": "Minimum spanning forest via Prim; disconnected graphs yield a forest.",
    },
    "kruskal": {
        "traced": kruskal_traced,
        "plain": kruskal,
        "time": "O(E log E)",
        "space": "O(V)",
        "description": "Minimum spanning forest via Kruskal and union-find.",
    },
    "topological_sort": {
        "traced": topological_sort_traced,
        "plain": topological_sort,
        "time": "O(V + E)",
        "space": "O(V)",
        "description": "Topological order via DFS; plain returns [] if a cycle exists.",
    },
}
