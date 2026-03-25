from __future__ import annotations

import math
from collections.abc import Iterator
from typing import Any, TypedDict


class MergeSortStep(TypedDict):
    array: list[int]
    left: list[int]
    right: list[int]
    merging: bool
    depth: int
    step: int


class ClosestPairStep(TypedDict):
    points: list[tuple[float, float]]
    strip: list[tuple[float, float]]
    closest_pair: tuple[tuple[float, float], tuple[float, float]] | None
    min_dist: float
    step: int


class KaratsubaStep(TypedDict):
    x: int
    y: int
    sub_products: dict[str, int]
    result: int
    depth: int
    step: int


def merge_sort_traced(arr: list[int]) -> Iterator[MergeSortStep]:
    a = list(arr)
    step = 0

    def emit(
        left: list[int],
        right: list[int],
        merging: bool,
        depth: int,
    ) -> MergeSortStep:
        nonlocal step
        step += 1
        return {
            "array": list(a),
            "left": list(left),
            "right": list(right),
            "merging": merging,
            "depth": depth,
            "step": step,
        }

    def sort_range(lo: int, hi: int, depth: int) -> None:
        if hi - lo <= 1:
            return
        mid = (lo + hi) // 2
        yield emit(a[lo:mid], a[mid:hi], False, depth)
        yield from sort_range(lo, mid, depth + 1)
        yield from sort_range(mid, hi, depth + 1)
        i, j, k = lo, mid, lo
        left_copy = a[lo:mid]
        right_copy = a[mid:hi]
        yield emit(left_copy, right_copy, True, depth)
        while i < mid and j < hi:
            if a[i] <= a[j]:
                a[k] = a[i]
                i += 1
            else:
                a[k] = a[j]
                j += 1
            k += 1
            yield emit(left_copy, right_copy, True, depth)
        while i < mid:
            a[k] = a[i]
            i += 1
            k += 1
            yield emit(left_copy, right_copy, True, depth)
        while j < hi:
            a[k] = a[j]
            j += 1
            k += 1
            yield emit(left_copy, right_copy, True, depth)

    if len(a) <= 1:
        step += 1
        yield {
            "array": list(a),
            "left": [],
            "right": [],
            "merging": False,
            "depth": 0,
            "step": step,
        }
        return

    gen = sort_range(0, len(a), 0)
    yield from gen


def merge_sort_plain(arr: list[int]) -> list[int]:
    a = list(arr)

    def merge(lo: int, mid: int, hi: int) -> None:
        i, j, k = lo, mid, lo
        left = a[lo:mid]
        right = a[mid:hi]
        li, lj = 0, 0
        while li < len(left) and lj < len(right):
            if left[li] <= right[lj]:
                a[k] = left[li]
                li += 1
            else:
                a[k] = right[lj]
                lj += 1
            k += 1
        while li < len(left):
            a[k] = left[li]
            li += 1
            k += 1
        while lj < len(right):
            a[k] = right[lj]
            lj += 1
            k += 1

    def sort(lo: int, hi: int) -> None:
        if hi - lo <= 1:
            return
        mid = (lo + hi) // 2
        sort(lo, mid)
        sort(mid, hi)
        merge(lo, mid, hi)

    sort(0, len(a))
    return a


def _dist(p: tuple[float, float], q: tuple[float, float]) -> float:
    return math.hypot(p[0] - q[0], p[1] - q[1])


def _brutal_closest(pts: list[tuple[float, float]]) -> tuple[float, tuple[float, float], tuple[float, float]]:
    if len(pts) < 2:
        p0 = pts[0] if pts else (0.0, 0.0)
        return float("inf"), p0, p0
    best = float("inf")
    pair = (pts[0], pts[1])
    for i in range(len(pts)):
        for j in range(i + 1, len(pts)):
            d = _dist(pts[i], pts[j])
            if d < best:
                best = d
                pair = (pts[i], pts[j])
    return best, pair[0], pair[1]


def closest_pair_traced(points: list[tuple[float, float]]) -> Iterator[ClosestPairStep]:
    step = 0
    pts = list(points)
    if len(pts) < 2:
        step += 1
        yield {
            "points": list(pts),
            "strip": [],
            "closest_pair": None,
            "min_dist": float("inf"),
            "step": step,
        }
        return

    ix_x = sorted(range(len(pts)), key=lambda i: pts[i][0])

    def coords(ii: list[int]) -> list[tuple[float, float]]:
        return [pts[i] for i in ii]

    def emit(
        ii: list[int],
        strip_pts: list[tuple[float, float]],
        cp: tuple[tuple[float, float], tuple[float, float]] | None,
        md: float,
    ) -> ClosestPairStep:
        nonlocal step
        step += 1
        return {
            "points": coords(ii),
            "strip": list(strip_pts),
            "closest_pair": cp,
            "min_dist": md,
            "step": step,
        }

    def rec(ix: list[int]) -> Iterator[ClosestPairStep]:
        n = len(ix)
        iy = sorted(ix, key=lambda i: pts[i][1])
        if n <= 3:
            sub = coords(ix)
            md, p1, p2 = _brutal_closest(sub)
            yield emit(ix, [], (p1, p2), md)
            return md, p1, p2
        mid = n // 2
        mid_x = pts[ix[mid]][0]
        left_ix = ix[:mid]
        right_ix = ix[mid:]
        yield emit(ix, [], None, float("inf"))
        gl = rec(left_ix)
        while True:
            try:
                yield next(gl)
            except StopIteration as e:
                dl, l1, l2 = e.value
                break
        gr = rec(right_ix)
        while True:
            try:
                yield next(gr)
            except StopIteration as e:
                dr, r1, r2 = e.value
                break
        if dl <= dr:
            d, b1, b2 = dl, l1, l2
        else:
            d, b1, b2 = dr, r1, r2
        strip_idx = [i for i in iy if abs(pts[i][0] - mid_x) < d]
        strip_pts = [pts[i] for i in strip_idx]
        yield emit(ix, strip_pts, (b1, b2), d)
        for si in range(len(strip_idx)):
            i = strip_idx[si]
            sj = si + 1
            while sj < len(strip_idx) and pts[strip_idx[sj]][1] - pts[i][1] < d:
                j = strip_idx[sj]
                dd = _dist(pts[i], pts[j])
                if dd < d:
                    d = dd
                    b1, b2 = pts[i], pts[j]
                    yield emit(ix, strip_pts, (b1, b2), d)
                sj += 1
        return d, b1, b2

    g = rec(ix_x)
    while True:
        try:
            yield next(g)
        except StopIteration:
            break


def closest_pair_plain(points: list[tuple[float, float]]) -> tuple[tuple[float, float], tuple[float, float]] | None:
    pts = list(points)
    if len(pts) < 2:
        return None
    ix_x = sorted(range(len(pts)), key=lambda i: pts[i][0])

    def rec(ix: list[int]) -> tuple[float, tuple[float, float], tuple[float, float]]:
        n = len(ix)
        iy = sorted(ix, key=lambda i: pts[i][1])
        if n <= 3:
            return _brutal_closest([pts[i] for i in ix])
        mid = n // 2
        mid_x = pts[ix[mid]][0]
        left_ix = ix[:mid]
        right_ix = ix[mid:]
        dl, l1, l2 = rec(left_ix)
        dr, r1, r2 = rec(right_ix)
        if dl <= dr:
            d, b1, b2 = dl, l1, l2
        else:
            d, b1, b2 = dr, r1, r2
        strip_idx = [i for i in iy if abs(pts[i][0] - mid_x) < d]
        for si in range(len(strip_idx)):
            i = strip_idx[si]
            sj = si + 1
            while sj < len(strip_idx) and pts[strip_idx[sj]][1] - pts[i][1] < d:
                j = strip_idx[sj]
                dd = _dist(pts[i], pts[j])
                if dd < d:
                    d, b1, b2 = dd, pts[i], pts[j]
                sj += 1
        return d, b1, b2

    _, p1, p2 = rec(ix_x)
    return (p1, p2)


def karatsuba_traced(x: int, y: int) -> Iterator[KaratsubaStep]:
    if x < 0 or y < 0:
        yield {
            "x": x,
            "y": y,
            "sub_products": {},
            "result": x * y,
            "depth": 0,
            "step": 1,
        }
        return
    step = 0

    def emit(
        xx: int,
        yy: int,
        subs: dict[str, int],
        res: int,
        depth: int,
    ) -> KaratsubaStep:
        nonlocal step
        step += 1
        return {
            "x": xx,
            "y": yy,
            "sub_products": dict(subs),
            "result": res,
            "depth": depth,
            "step": step,
        }

    def rec(xx: int, yy: int, depth: int) -> Iterator[KaratsubaStep]:
        if xx < 2**16 and yy < 2**16:
            r = xx * yy
            yield emit(xx, yy, {}, r, depth)
            return r
        m = max(xx.bit_length(), yy.bit_length()) // 2
        split = 1 << m
        a, b = xx // split, xx % split
        c, d = yy // split, yy % split
        yield emit(xx, yy, {"a": a, "b": b, "c": c, "d": d, "m_bits": m}, 0, depth)
        z2_gen = rec(a, c, depth + 1)
        z2 = 0
        while True:
            try:
                yield next(z2_gen)
            except StopIteration as e:
                z2 = int(e.value)
                break
        z0_gen = rec(b, d, depth + 1)
        z0 = 0
        while True:
            try:
                yield next(z0_gen)
            except StopIteration as e:
                z0 = int(e.value)
                break
        z1_gen = rec(a + b, c + d, depth + 1)
        z1_full = 0
        while True:
            try:
                yield next(z1_gen)
            except StopIteration as e:
                z1_full = int(e.value)
                break
        z1 = z1_full - z0 - z2
        r = z2 * (split * split) + z1 * split + z0
        yield emit(
            xx,
            yy,
            {"z0": z0, "z1": z1, "z2": z2, "m_bits": m},
            r,
            depth,
        )
        return r

    g = rec(x, y, 0)
    while True:
        try:
            yield next(g)
        except StopIteration:
            break


def _karatsuba_nonneg(x: int, y: int) -> int:
    if x < 2**16 and y < 2**16:
        return x * y
    m = max(x.bit_length(), y.bit_length()) // 2
    split = 1 << m
    a, b = x // split, x % split
    c, d = y // split, y % split
    z2 = _karatsuba_nonneg(a, c)
    z0 = _karatsuba_nonneg(b, d)
    z1 = _karatsuba_nonneg(a + b, c + d) - z0 - z2
    return z2 * (split * split) + z1 * split + z0


def karatsuba_plain(x: int, y: int) -> int:
    s = (1 if x >= 0 else -1) * (1 if y >= 0 else -1)
    return s * _karatsuba_nonneg(abs(x), abs(y))


ALGORITHMS: dict[str, dict[str, Any]] = {
    "merge_sort": {
        "traced": merge_sort_traced,
        "plain": merge_sort_plain,
        "time": "O(n log n)",
        "space": "O(n)",
        "description": "Sort by recursively splitting and merging sorted runs.",
    },
    "closest_pair": {
        "traced": closest_pair_traced,
        "plain": closest_pair_plain,
        "time": "O(n log n)",
        "space": "O(n)",
        "description": "Pasangan titik terdekat di bidang dengan divide and conquer.",
    },
    "karatsuba": {
        "traced": karatsuba_traced,
        "plain": karatsuba_plain,
        "time": "O(n^log2(3))",
        "space": "O(log n)",
        "description": "Integer multiply with three recursive half-size products.",
    },
}
