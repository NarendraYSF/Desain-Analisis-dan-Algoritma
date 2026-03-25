from __future__ import annotations

from collections.abc import Iterator
from typing import Callable, TypedDict


class SortStep(TypedDict, total=False):
    array: list[int]
    comparing: tuple[int, int] | None
    swapped: tuple[int, int] | None
    sorted_indices: list[int]
    comparisons: int
    swaps: int


class AlgorithmMeta(TypedDict):
    traced: Callable[[list[int]], Iterator[SortStep]]
    plain: Callable[[list[int]], list[int]]
    time: str
    space: str
    stable: bool


def _emit(
    a: list[int],
    *,
    comparing: tuple[int, int] | None = None,
    swapped: tuple[int, int] | None = None,
    sorted_indices: list[int] | None = None,
    comparisons: int = 0,
    swaps: int = 0,
) -> SortStep:
    return {
        "array": list(a),
        "comparing": comparing,
        "swapped": swapped,
        "sorted_indices": list(sorted_indices) if sorted_indices is not None else [],
        "comparisons": comparisons,
        "swaps": swaps,
    }


def bubble_sort_traced(arr: list[int]) -> Iterator[SortStep]:
    a = list(arr)
    n = len(a)
    comps = swaps_count = 0
    if n <= 1:
        yield _emit(a, sorted_indices=list(range(n)), comparisons=comps, swaps=swaps_count)
        return
    for i in range(n):
        swapped_any = False
        for j in range(n - 1 - i):
            comps += 1
            yield _emit(
                a,
                comparing=(j, j + 1),
                swapped=None,
                sorted_indices=list(range(n - i, n)),
                comparisons=comps,
                swaps=swaps_count,
            )
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swaps_count += 1
                swapped_any = True
                yield _emit(
                    a,
                    comparing=(j, j + 1),
                    swapped=(j, j + 1),
                    sorted_indices=list(range(n - i, n)),
                    comparisons=comps,
                    swaps=swaps_count,
                )
        if not swapped_any:
            break
    yield _emit(a, comparing=None, swapped=None, sorted_indices=list(range(n)), comparisons=comps, swaps=swaps_count)


def bubble_sort_plain(arr: list[int]) -> list[int]:
    a = list(arr)
    n = len(a)
    for i in range(n):
        swapped_any = False
        for j in range(n - 1 - i):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swapped_any = True
        if not swapped_any:
            break
    return a


def selection_sort_traced(arr: list[int]) -> Iterator[SortStep]:
    a = list(arr)
    n = len(a)
    comps = swaps_count = 0
    if n <= 1:
        yield _emit(a, sorted_indices=list(range(n)), comparisons=comps, swaps=swaps_count)
        return
    for i in range(n):
        min_i = i
        for j in range(i + 1, n):
            comps += 1
            yield _emit(
                a,
                comparing=(min_i, j),
                swapped=None,
                sorted_indices=list(range(i)),
                comparisons=comps,
                swaps=swaps_count,
            )
            if a[j] < a[min_i]:
                min_i = j
        if min_i != i:
            a[i], a[min_i] = a[min_i], a[i]
            swaps_count += 1
            yield _emit(
                a,
                comparing=(i, min_i),
                swapped=(i, min_i),
                sorted_indices=list(range(i)),
                comparisons=comps,
                swaps=swaps_count,
            )
        else:
            yield _emit(
                a,
                comparing=None,
                swapped=None,
                sorted_indices=list(range(i + 1)),
                comparisons=comps,
                swaps=swaps_count,
            )
    yield _emit(a, comparing=None, swapped=None, sorted_indices=list(range(n)), comparisons=comps, swaps=swaps_count)


def selection_sort_plain(arr: list[int]) -> list[int]:
    a = list(arr)
    n = len(a)
    for i in range(n):
        min_i = i
        for j in range(i + 1, n):
            if a[j] < a[min_i]:
                min_i = j
        if min_i != i:
            a[i], a[min_i] = a[min_i], a[i]
    return a


def insertion_sort_traced(arr: list[int]) -> Iterator[SortStep]:
    a = list(arr)
    n = len(a)
    comps = swaps_count = 0
    if n <= 1:
        yield _emit(a, sorted_indices=list(range(n)), comparisons=comps, swaps=swaps_count)
        return
    yield _emit(a, comparing=None, swapped=None, sorted_indices=[0], comparisons=comps, swaps=swaps_count)
    for i in range(1, n):
        key = a[i]
        j = i - 1
        while j >= 0:
            comps += 1
            yield _emit(
                a,
                comparing=(j, j + 1),
                swapped=None,
                sorted_indices=list(range(i)),
                comparisons=comps,
                swaps=swaps_count,
            )
            if a[j] > key:
                a[j + 1] = a[j]
                swaps_count += 1
                yield _emit(
                    a,
                    comparing=(j, j + 1),
                    swapped=(j, j + 1),
                    sorted_indices=list(range(i)),
                    comparisons=comps,
                    swaps=swaps_count,
                )
                j -= 1
            else:
                break
        a[j + 1] = key
        yield _emit(
            a,
            comparing=None,
            swapped=None,
            sorted_indices=list(range(i + 1)),
            comparisons=comps,
            swaps=swaps_count,
        )
    yield _emit(a, comparing=None, swapped=None, sorted_indices=list(range(n)), comparisons=comps, swaps=swaps_count)


def insertion_sort_plain(arr: list[int]) -> list[int]:
    a = list(arr)
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
    return a


def merge_sort_traced(arr: list[int]) -> Iterator[SortStep]:
    a = list(arr)
    n = len(a)
    comps = [0]
    swaps_count = [0]
    if n <= 1:
        yield _emit(a, sorted_indices=list(range(n)), comparisons=0, swaps=0)
        return

    def sort_range(left: int, right: int) -> Iterator[SortStep]:
        if right - left <= 1:
            return
        mid = (left + right) // 2
        yield from sort_range(left, mid)
        yield from sort_range(mid, right)
        buf = a[left:right]
        nL, nR = mid - left, right - mid
        p, q, k = 0, 0, left
        while p < nL and q < nR:
            comps[0] += 1
            yield _emit(
                a,
                comparing=(left + p, mid + q),
                swapped=None,
                sorted_indices=[],
                comparisons=comps[0],
                swaps=swaps_count[0],
            )
            if buf[p] <= buf[nL + q]:
                val = buf[p]
                p += 1
            else:
                val = buf[nL + q]
                q += 1
            changed = a[k] != val
            a[k] = val
            if changed:
                swaps_count[0] += 1
            yield _emit(
                a,
                comparing=None,
                swapped=(k, k) if changed else None,
                sorted_indices=[],
                comparisons=comps[0],
                swaps=swaps_count[0],
            )
            k += 1
        while p < nL:
            val = buf[p]
            p += 1
            changed = a[k] != val
            a[k] = val
            if changed:
                swaps_count[0] += 1
            yield _emit(
                a,
                comparing=None,
                swapped=(k, k) if changed else None,
                sorted_indices=[],
                comparisons=comps[0],
                swaps=swaps_count[0],
            )
            k += 1
        while q < nR:
            val = buf[nL + q]
            q += 1
            changed = a[k] != val
            a[k] = val
            if changed:
                swaps_count[0] += 1
            yield _emit(
                a,
                comparing=None,
                swapped=(k, k) if changed else None,
                sorted_indices=[],
                comparisons=comps[0],
                swaps=swaps_count[0],
            )
            k += 1

    yield from sort_range(0, n)
    yield _emit(
        a,
        comparing=None,
        swapped=None,
        sorted_indices=list(range(n)),
        comparisons=comps[0],
        swaps=swaps_count[0],
    )


def merge_sort_plain(arr: list[int]) -> list[int]:
    a = list(arr)

    def merge(left: int, mid: int, right: int) -> None:
        buf = a[left:right]
        nL, nR = mid - left, right - mid
        p, q, k = 0, 0, left
        while p < nL and q < nR:
            if buf[p] <= buf[nL + q]:
                a[k] = buf[p]
                p += 1
            else:
                a[k] = buf[nL + q]
                q += 1
            k += 1
        while p < nL:
            a[k] = buf[p]
            p += 1
            k += 1
        while q < nR:
            a[k] = buf[nL + q]
            q += 1
            k += 1

    def sort_range(left: int, right: int) -> None:
        if right - left <= 1:
            return
        mid = (left + right) // 2
        sort_range(left, mid)
        sort_range(mid, right)
        merge(left, mid, right)

    sort_range(0, len(a))
    return a


def quick_sort_traced(arr: list[int]) -> Iterator[SortStep]:
    a = list(arr)
    n = len(a)
    comps = [0]
    swaps_count = [0]
    if n <= 1:
        yield _emit(a, sorted_indices=list(range(n)), comparisons=0, swaps=0)
        return

    def qs(lo: int, hi: int) -> Iterator[SortStep]:
        if lo >= hi:
            return
        pivot = a[hi]
        i = lo - 1
        for j in range(lo, hi):
            comps[0] += 1
            yield _emit(
                a,
                comparing=(j, hi),
                swapped=None,
                sorted_indices=[],
                comparisons=comps[0],
                swaps=swaps_count[0],
            )
            if a[j] <= pivot:
                i += 1
                if i != j:
                    a[i], a[j] = a[j], a[i]
                    swaps_count[0] += 1
                    yield _emit(
                        a,
                        comparing=(i, j),
                        swapped=(i, j),
                        sorted_indices=[],
                        comparisons=comps[0],
                        swaps=swaps_count[0],
                    )
        if i + 1 != hi:
            a[i + 1], a[hi] = a[hi], a[i + 1]
            swaps_count[0] += 1
            yield _emit(
                a,
                comparing=(i + 1, hi),
                swapped=(i + 1, hi),
                sorted_indices=[],
                comparisons=comps[0],
                swaps=swaps_count[0],
            )
        p = i + 1
        yield from qs(lo, p - 1)
        yield from qs(p + 1, hi)

    yield from qs(0, n - 1)
    yield _emit(
        a,
        comparing=None,
        swapped=None,
        sorted_indices=list(range(n)),
        comparisons=comps[0],
        swaps=swaps_count[0],
    )


def quick_sort_plain(arr: list[int]) -> list[int]:
    a = list(arr)

    def qs(lo: int, hi: int) -> None:
        if lo >= hi:
            return
        pivot = a[hi]
        i = lo - 1
        for j in range(lo, hi):
            if a[j] <= pivot:
                i += 1
                a[i], a[j] = a[j], a[i]
        a[i + 1], a[hi] = a[hi], a[i + 1]
        p = i + 1
        qs(lo, p - 1)
        qs(p + 1, hi)

    if a:
        qs(0, len(a) - 1)
    return a


def _sift_down_traced(
    a: list[int],
    heap_size: int,
    i: int,
    comps: list[int],
    swaps_count: list[int],
    total_n: int,
    sorted_start: int | None,
) -> Iterator[SortStep]:
    def suffix() -> list[int]:
        if sorted_start is None or sorted_start >= total_n:
            return []
        return list(range(sorted_start, total_n))

    while True:
        largest = i
        l = 2 * i + 1
        r = 2 * i + 2
        if l < heap_size:
            comps[0] += 1
            yield _emit(
                a,
                comparing=(largest, l),
                swapped=None,
                sorted_indices=suffix(),
                comparisons=comps[0],
                swaps=swaps_count[0],
            )
            if a[l] > a[largest]:
                largest = l
        if r < heap_size:
            comps[0] += 1
            yield _emit(
                a,
                comparing=(largest, r),
                swapped=None,
                sorted_indices=suffix(),
                comparisons=comps[0],
                swaps=swaps_count[0],
            )
            if a[r] > a[largest]:
                largest = r
        if largest != i:
            a[i], a[largest] = a[largest], a[i]
            swaps_count[0] += 1
            yield _emit(
                a,
                comparing=(i, largest),
                swapped=(i, largest),
                sorted_indices=suffix(),
                comparisons=comps[0],
                swaps=swaps_count[0],
            )
            i = largest
        else:
            break


def heap_sort_traced(arr: list[int]) -> Iterator[SortStep]:
    a = list(arr)
    n = len(a)
    comps = [0]
    swaps_count = [0]
    if n <= 1:
        yield _emit(a, sorted_indices=list(range(n)), comparisons=0, swaps=0)
        return
    for i in range(n // 2 - 1, -1, -1):
        yield from _sift_down_traced(a, n, i, comps, swaps_count, n, None)
    for end in range(n - 1, 0, -1):
        a[0], a[end] = a[end], a[0]
        swaps_count[0] += 1
        yield _emit(
            a,
            comparing=(0, end),
            swapped=(0, end),
            sorted_indices=list(range(end, n)),
            comparisons=comps[0],
            swaps=swaps_count[0],
        )
        yield from _sift_down_traced(a, end, 0, comps, swaps_count, n, end)
    yield _emit(
        a,
        comparing=None,
        swapped=None,
        sorted_indices=list(range(n)),
        comparisons=comps[0],
        swaps=swaps_count[0],
    )


def heap_sort_plain(arr: list[int]) -> list[int]:
    a = list(arr)
    n = len(a)

    def sift(i: int, size: int) -> None:
        while True:
            largest = i
            l, r = 2 * i + 1, 2 * i + 2
            if l < size and a[l] > a[largest]:
                largest = l
            if r < size and a[r] > a[largest]:
                largest = r
            if largest != i:
                a[i], a[largest] = a[largest], a[i]
                i = largest
            else:
                break

    for i in range(n // 2 - 1, -1, -1):
        sift(i, n)
    for end in range(n - 1, 0, -1):
        a[0], a[end] = a[end], a[0]
        sift(0, end)
    return a


def counting_sort_traced(arr: list[int]) -> Iterator[SortStep]:
    a = list(arr)
    n = len(a)
    comps = 0
    swaps_count = 0
    if n == 0:
        yield _emit(a, sorted_indices=[], comparisons=0, swaps=0)
        return
    mn, mx = min(a), max(a)
    rng = mx - mn + 1
    count = [0] * rng
    for idx, x in enumerate(a):
        comps += 1
        yield _emit(
            a,
            comparing=(idx, idx),
            swapped=None,
            sorted_indices=[],
            comparisons=comps,
            swaps=swaps_count,
        )
        count[x - mn] += 1
    for i in range(1, rng):
        count[i] += count[i - 1]
    empty = mn - 1
    out = [empty] * n
    for idx in range(n - 1, -1, -1):
        x = a[idx]
        comps += 1
        yield _emit(
            a,
            comparing=(idx, idx),
            swapped=None,
            sorted_indices=[],
            comparisons=comps,
            swaps=swaps_count,
        )
        pos = count[x - mn] - 1
        count[x - mn] -= 1
        out[pos] = x
        swaps_count += 1
        yield _emit(
            out,
            comparing=(idx, pos),
            swapped=(idx, pos),
            sorted_indices=[],
            comparisons=comps,
            swaps=swaps_count,
        )
    yield _emit(
        out,
        comparing=None,
        swapped=None,
        sorted_indices=list(range(n)),
        comparisons=comps,
        swaps=swaps_count,
    )


def counting_sort_plain(arr: list[int]) -> list[int]:
    a = list(arr)
    n = len(a)
    if n == 0:
        return []
    mn, mx = min(a), max(a)
    rng = mx - mn + 1
    count = [0] * rng
    for x in a:
        count[x - mn] += 1
    for i in range(1, rng):
        count[i] += count[i - 1]
    out = [0] * n
    for x in reversed(a):
        pos = count[x - mn] - 1
        count[x - mn] -= 1
        out[pos] = x
    return out


def _radix_digit(value: int, exp: int, base: int) -> int:
    return (value // exp) % base


def radix_sort_traced(arr: list[int], base: int = 10) -> Iterator[SortStep]:
    a = list(arr)
    n = len(a)
    comps = 0
    swaps_count = 0
    if n == 0:
        yield _emit(a, sorted_indices=[], comparisons=0, swaps=0)
        return
    if any(x < 0 for x in a):
        raise ValueError("radix_sort_traced requires non-negative integers")
    mx = max(a)
    exp = 1
    while mx // exp > 0:
        rng = base
        count = [0] * rng
        for idx, x in enumerate(a):
            comps += 1
            d = _radix_digit(x, exp, base)
            yield _emit(
                a,
                comparing=(idx, idx),
                swapped=None,
                sorted_indices=[],
                comparisons=comps,
                swaps=swaps_count,
            )
            count[d] += 1
        for i in range(1, rng):
            count[i] += count[i - 1]
        empty = -1
        out = [empty] * n
        for idx in range(n - 1, -1, -1):
            x = a[idx]
            comps += 1
            d = _radix_digit(x, exp, base)
            yield _emit(
                a,
                comparing=(idx, idx),
                swapped=None,
                sorted_indices=[],
                comparisons=comps,
                swaps=swaps_count,
            )
            pos = count[d] - 1
            count[d] -= 1
            out[pos] = x
            swaps_count += 1
            yield _emit(
                out,
                comparing=(idx, pos),
                swapped=(idx, pos),
                sorted_indices=[],
                comparisons=comps,
                swaps=swaps_count,
            )
        a = out
        exp *= base
    yield _emit(
        a,
        comparing=None,
        swapped=None,
        sorted_indices=list(range(n)),
        comparisons=comps,
        swaps=swaps_count,
    )


def radix_sort_plain(arr: list[int], base: int = 10) -> list[int]:
    a = list(arr)
    if not a:
        return []
    if any(x < 0 for x in a):
        raise ValueError("radix_sort_plain requires non-negative integers")
    mx = max(a)
    exp = 1
    while mx // exp > 0:
        rng = base
        count = [0] * rng
        for x in a:
            count[_radix_digit(x, exp, base)] += 1
        for i in range(1, rng):
            count[i] += count[i - 1]
        out = [0] * len(a)
        for x in reversed(a):
            d = _radix_digit(x, exp, base)
            pos = count[d] - 1
            count[d] -= 1
            out[pos] = x
        a = out
        exp *= base
    return a


def _radix_sort_traced_adapter(arr: list[int]) -> Iterator[SortStep]:
    return radix_sort_traced(arr, base=10)


def _radix_sort_plain_adapter(arr: list[int]) -> list[int]:
    return radix_sort_plain(arr, base=10)


ALGORITHMS: dict[str, AlgorithmMeta] = {
    "bubble": {
        "traced": bubble_sort_traced,
        "plain": bubble_sort_plain,
        "time": "O(n^2)",
        "space": "O(1)",
        "stable": True,
    },
    "selection": {
        "traced": selection_sort_traced,
        "plain": selection_sort_plain,
        "time": "O(n^2)",
        "space": "O(1)",
        "stable": False,
    },
    "insertion": {
        "traced": insertion_sort_traced,
        "plain": insertion_sort_plain,
        "time": "O(n^2)",
        "space": "O(1)",
        "stable": True,
    },
    "merge": {
        "traced": merge_sort_traced,
        "plain": merge_sort_plain,
        "time": "O(n log n)",
        "space": "O(n)",
        "stable": True,
    },
    "quick": {
        "traced": quick_sort_traced,
        "plain": quick_sort_plain,
        "time": "O(n log n) average, O(n^2) worst",
        "space": "O(log n)",
        "stable": False,
    },
    "heap": {
        "traced": heap_sort_traced,
        "plain": heap_sort_plain,
        "time": "O(n log n)",
        "space": "O(1)",
        "stable": False,
    },
    "counting": {
        "traced": counting_sort_traced,
        "plain": counting_sort_plain,
        "time": "O(n + k)",
        "space": "O(k)",
        "stable": True,
    },
    "radix": {
        "traced": _radix_sort_traced_adapter,
        "plain": _radix_sort_plain_adapter,
        "time": "O(d * (n + b))",
        "space": "O(n + b)",
        "stable": True,
    },
}


def _self_check() -> None:
    samples = [
        [],
        [1],
        [3, 1, 4, 1, 5, 9, 2, 6],
        [5, 4, 3, 2, 1],
        [1, 2, 3, 4],
    ]
    for name, meta in ALGORITHMS.items():
        plain = meta["plain"]
        for s in samples:
            if name == "radix" and any(x < 0 for x in s):
                continue
            got = plain(list(s))
            assert got == sorted(s), (name, s, got)
    for s in [[3, 1, 4], [0, 0, 1], [10, 2, 5]]:
        list(merge_sort_traced(s))
        list(quick_sort_traced(s))


if __name__ == "__main__":
    _self_check()
