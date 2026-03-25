from __future__ import annotations

from typing import Any, Dict, Generator, List, Optional


def _state(
    array: List[Any],
    target: Any,
    checking: int,
    low: int,
    high: int,
    found: Optional[bool],
    comparisons: int,
    step: int,
) -> Dict[str, Any]:
    return {
        "array": list(array),
        "target": target,
        "checking": checking,
        "low": low,
        "high": high,
        "found": found,
        "comparisons": comparisons,
        "step": step,
    }


def linear_search_traced(
    array: List[Any], target: Any
) -> Generator[Dict[str, Any], None, None]:
    n = len(array)
    comparisons = 0
    step = 0
    low, high = 0, n - 1 if n else -1
    if n == 0:
        yield _state(array, target, -1, low, high, False, comparisons, step)
        return
    for i in range(n):
        comparisons += 1
        yield _state(array, target, i, low, high, None, comparisons, step)
        step += 1
        if array[i] == target:
            yield _state(array, target, i, low, high, True, comparisons, step)
            return
    yield _state(array, target, n - 1, low, high, False, comparisons, step)


def linear_search(array: List[Any], target: Any) -> int:
    for i, x in enumerate(array):
        if x == target:
            return i
    return -1


def binary_search_traced(
    array: List[Any], target: Any
) -> Generator[Dict[str, Any], None, None]:
    comparisons = 0
    step = 0
    low, high = 0, len(array) - 1
    while low <= high:
        mid = (low + high) // 2
        comparisons += 1
        yield _state(array, target, mid, low, high, None, comparisons, step)
        step += 1
        if array[mid] == target:
            yield _state(array, target, mid, low, high, True, comparisons, step)
            return
        if array[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    checking = low if 0 <= low < len(array) else (high if high >= 0 else -1)
    yield _state(array, target, checking, low, high, False, comparisons, step)


def binary_search(array: List[Any], target: Any) -> int:
    low, high = 0, len(array) - 1
    while low <= high:
        mid = (low + high) // 2
        if array[mid] == target:
            return mid
        if array[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1


def interpolation_search_traced(
    array: List[Any], target: Any
) -> Generator[Dict[str, Any], None, None]:
    comparisons = 0
    step = 0
    low, high = 0, len(array) - 1
    if not array:
        yield _state(array, target, -1, low, high, False, comparisons, step)
        return
    while low <= high and array[low] <= target <= array[high]:
        if array[low] == array[high]:
            comparisons += 1
            yield _state(array, target, low, low, high, None, comparisons, step)
            step += 1
            if array[low] == target:
                yield _state(array, target, low, low, high, True, comparisons, step)
                return
            break
        pos = low + (target - array[low]) * (high - low) // (array[high] - array[low])
        pos = max(low, min(high, int(pos)))
        comparisons += 1
        yield _state(array, target, pos, low, high, None, comparisons, step)
        step += 1
        if array[pos] == target:
            yield _state(array, target, pos, low, high, True, comparisons, step)
            return
        if array[pos] < target:
            low = pos + 1
        else:
            high = pos - 1
    checking = low if 0 <= low < len(array) else (high if high >= 0 else -1)
    yield _state(array, target, checking, low, high, False, comparisons, step)


def interpolation_search(array: List[Any], target: Any) -> int:
    low, high = 0, len(array) - 1
    if not array:
        return -1
    while low <= high and array[low] <= target <= array[high]:
        if array[low] == array[high]:
            return low if array[low] == target else -1
        pos = low + (target - array[low]) * (high - low) // (array[high] - array[low])
        pos = max(low, min(high, int(pos)))
        if array[pos] == target:
            return pos
        if array[pos] < target:
            low = pos + 1
        else:
            high = pos - 1
    return -1


ALGORITHMS: Dict[str, Dict[str, Any]] = {
    "linear_search": {
        "traced": linear_search_traced,
        "plain": linear_search,
        "time_best": "O(1)",
        "time_avg": "O(n)",
        "time_worst": "O(n)",
        "space": "O(1)",
    },
    "binary_search": {
        "traced": binary_search_traced,
        "plain": binary_search,
        "time_best": "O(1)",
        "time_avg": "O(log n)",
        "time_worst": "O(log n)",
        "space": "O(1)",
    },
    "interpolation_search": {
        "traced": interpolation_search_traced,
        "plain": interpolation_search,
        "time_best": "O(1)",
        "time_avg": "O(log log n)",
        "time_worst": "O(n)",
        "space": "O(1)",
    },
}
