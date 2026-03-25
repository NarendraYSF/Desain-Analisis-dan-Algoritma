from __future__ import annotations

import heapq
from collections.abc import Iterator
from typing import Any, TypedDict


class ActivityStep(TypedDict):
    selected: list[tuple[int, int]]
    current: tuple[int, int] | None
    decision: str
    step: int


class KnapsackStep(TypedDict):
    items_taken: list[tuple[float, float, float]]
    current_item: tuple[float, float] | None
    remaining_capacity: float
    total_value: float
    step: int


class HuffmanStep(TypedDict):
    tree_nodes: list[dict[str, Any]]
    merged: tuple[dict[str, Any], dict[str, Any]] | None
    codes: dict[str, str]
    step: int


def _node_dict(
    char: str | None,
    freq: int,
    left: dict[str, Any] | None,
    right: dict[str, Any] | None,
) -> dict[str, Any]:
    return {"char": char, "freq": freq, "left": left, "right": right}


def _deep_node(n: dict[str, Any]) -> dict[str, Any]:
    return _node_dict(
        n.get("char"),
        int(n["freq"]),
        _deep_node(n["left"]) if n.get("left") is not None else None,
        _deep_node(n["right"]) if n.get("right") is not None else None,
    )


def _huffman_codes_from_tree(root: dict[str, Any]) -> dict[str, str]:
    out: dict[str, str] = {}

    def walk(n: dict[str, Any], prefix: str) -> None:
        ch = n.get("char")
        if ch is not None and n.get("left") is None and n.get("right") is None:
            out[ch] = "0" if prefix == "" else prefix
            return
        left, right = n.get("left"), n.get("right")
        if left is not None:
            walk(left, prefix + "0")
        if right is not None:
            walk(right, prefix + "1")

    walk(root, "")
    return out


def _forest_to_nodes(forest: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [_deep_node(n) for n in forest]


def activity_selection_traced(
    starts: list[int], finishes: list[int]
) -> Iterator[ActivityStep]:
    if len(starts) != len(finishes):
        raise ValueError("starts and finishes must have equal length")
    n = len(starts)
    step = 0
    if n == 0:
        yield {
            "selected": [],
            "current": None,
            "decision": "empty",
            "step": step,
        }
        return
    order = sorted(range(n), key=lambda i: finishes[i])
    selected: list[tuple[int, int]] = []
    last_finish = -1
    for idx in order:
        s, f = starts[idx], finishes[idx]
        step += 1
        if s >= last_finish:
            selected.append((s, f))
            last_finish = f
            yield {
                "selected": list(selected),
                "current": (s, f),
                "decision": "select",
                "step": step,
            }
        else:
            yield {
                "selected": list(selected),
                "current": (s, f),
                "decision": "reject_overlap",
                "step": step,
            }


def activity_selection_plain(starts: list[int], finishes: list[int]) -> list[tuple[int, int]]:
    if len(starts) != len(finishes):
        raise ValueError("starts and finishes must have equal length")
    n = len(starts)
    if n == 0:
        return []
    order = sorted(range(n), key=lambda i: finishes[i])
    selected: list[tuple[int, int]] = []
    last_finish = -1
    for idx in order:
        s, f = starts[idx], finishes[idx]
        if s >= last_finish:
            selected.append((s, f))
            last_finish = f
    return selected


def fractional_knapsack_traced(
    weights: list[float], values: list[float], capacity: float
) -> Iterator[KnapsackStep]:
    if len(weights) != len(values):
        raise ValueError("weights and values must have equal length")
    if capacity < 0:
        raise ValueError("capacity must be non-negative")
    step = 0
    items_taken: list[tuple[float, float, float]] = []
    total_value = 0.0
    remaining = float(capacity)
    n = len(weights)
    if n == 0:
        yield {
            "items_taken": [],
            "current_item": None,
            "remaining_capacity": remaining,
            "total_value": total_value,
            "step": step,
        }
        return

    def ratio(i: int) -> float:
        w = float(weights[i])
        if w <= 0:
            return float("-inf")
        return float(values[i]) / w

    idxs = sorted(range(n), key=ratio, reverse=True)
    for i in idxs:
        w, v = float(weights[i]), float(values[i])
        step += 1
        if w <= 0:
            yield {
                "items_taken": list(items_taken),
                "current_item": (w, v),
                "remaining_capacity": remaining,
                "total_value": total_value,
                "step": step,
            }
            continue
        if remaining <= 0:
            yield {
                "items_taken": list(items_taken),
                "current_item": (w, v),
                "remaining_capacity": remaining,
                "total_value": total_value,
                "step": step,
            }
            continue
        if w <= remaining:
            items_taken.append((w, v, 1.0))
            total_value += v
            remaining -= w
        else:
            frac = remaining / w
            items_taken.append((w, v, frac))
            total_value += v * frac
            remaining = 0.0
        yield {
            "items_taken": list(items_taken),
            "current_item": (w, v),
            "remaining_capacity": remaining,
            "total_value": total_value,
            "step": step,
        }


def fractional_knapsack_plain(
    weights: list[float], values: list[float], capacity: float
) -> tuple[float, list[tuple[float, float, float]]]:
    if len(weights) != len(values):
        raise ValueError("weights and values must have equal length")
    if capacity < 0:
        raise ValueError("capacity must be non-negative")
    items_taken: list[tuple[float, float, float]] = []
    total_value = 0.0
    remaining = float(capacity)
    n = len(weights)

    def ratio(i: int) -> float:
        w = float(weights[i])
        if w <= 0:
            return float("-inf")
        return float(values[i]) / w

    for i in sorted(range(n), key=ratio, reverse=True):
        w, v = float(weights[i]), float(values[i])
        if w <= 0 or remaining <= 0:
            continue
        if w <= remaining:
            items_taken.append((w, v, 1.0))
            total_value += v
            remaining -= w
        else:
            frac = remaining / w
            items_taken.append((w, v, frac))
            total_value += v * frac
            remaining = 0.0
    return total_value, items_taken


def huffman_traced(chars: list[str], freqs: list[int]) -> Iterator[HuffmanStep]:
    if len(chars) != len(freqs):
        raise ValueError("chars and freqs must have equal length")
    step = 0
    if not chars:
        yield {
            "tree_nodes": [],
            "merged": None,
            "codes": {},
            "step": step,
        }
        return
    heap: list[tuple[int, int, dict[str, Any]]] = []
    for i, (c, f) in enumerate(zip(chars, freqs, strict=True)):
        node = _node_dict(c, int(f), None, None)
        heapq.heappush(heap, (node["freq"], i, node))
    next_id = len(chars)
    if len(heap) == 1:
        root = heap[0][2]
        step = 1
        yield {
            "tree_nodes": _forest_to_nodes([root]),
            "merged": None,
            "codes": _huffman_codes_from_tree(root),
            "step": step,
        }
        return
    while len(heap) > 1:
        f1, _, left = heapq.heappop(heap)
        f2, _, right = heapq.heappop(heap)
        parent = _node_dict(None, f1 + f2, left, right)
        heapq.heappush(heap, (parent["freq"], next_id, parent))
        next_id += 1
        step += 1
        roots = [t[2] for t in sorted(heap, key=lambda t: (t[0], t[1]))]
        yield {
            "tree_nodes": _forest_to_nodes(roots),
            "merged": (_deep_node(left), _deep_node(right)),
            "codes": {},
            "step": step,
        }
    root = heap[0][2]
    step += 1
    yield {
        "tree_nodes": _forest_to_nodes([root]),
        "merged": None,
        "codes": _huffman_codes_from_tree(root),
        "step": step,
    }


def huffman_plain(chars: list[str], freqs: list[int]) -> dict[str, str]:
    if len(chars) != len(freqs):
        raise ValueError("chars and freqs must have equal length")
    if not chars:
        return {}
    heap: list[tuple[int, int, dict[str, Any]]] = []
    for i, (c, f) in enumerate(zip(chars, freqs, strict=True)):
        node = _node_dict(c, int(f), None, None)
        heapq.heappush(heap, (node["freq"], i, node))
    next_id = len(chars)
    if len(heap) == 1:
        return _huffman_codes_from_tree(heap[0][2])
    while len(heap) > 1:
        f1, _, left = heapq.heappop(heap)
        f2, _, right = heapq.heappop(heap)
        parent = _node_dict(None, f1 + f2, left, right)
        heapq.heappush(heap, (parent["freq"], next_id, parent))
        next_id += 1
    return _huffman_codes_from_tree(heap[0][2])


ALGORITHMS: dict[str, dict[str, Any]] = {
    "activity_selection": {
        "traced": activity_selection_traced,
        "plain": activity_selection_plain,
        "time": "O(n log n)",
        "space": "O(n)",
        "description": "Maximum-size compatible activity set by sorting on finish times.",
    },
    "fractional_knapsack": {
        "traced": fractional_knapsack_traced,
        "plain": fractional_knapsack_plain,
        "time": "O(n log n)",
        "space": "O(n)",
        "description": "Fractional knapsack by value-to-weight ratio.",
    },
    "huffman": {
        "traced": huffman_traced,
        "plain": huffman_plain,
        "time": "O(n log n)",
        "space": "O(n)",
        "description": "Build a Huffman tree for optimal prefix-free codes.",
    },
}
