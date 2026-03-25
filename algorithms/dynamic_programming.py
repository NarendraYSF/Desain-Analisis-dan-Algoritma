from __future__ import annotations

from typing import Any, Dict, Generator, List, Optional, Tuple, Union

Table = Union[List[List[Any]], List[Any]]
TraceYield = Dict[str, Any]

AlgorithmEntry = Dict[str, Any]


def _copy_table_2d(t: List[List[Any]]) -> List[List[Any]]:
    return [list(r) for r in t]


def _copy_table_1d(t: List[Any]) -> List[Any]:
    return list(t)


def knapsack_01_traced(
    weights: List[int], values: List[int], capacity: int
) -> Generator[TraceYield, None, None]:
    n = len(weights)
    dp: List[List[int]] = [[0] * (capacity + 1) for _ in range(n + 1)]
    step = 0
    for i in range(1, n + 1):
        for w in range(1, capacity + 1):
            step += 1
            wi, vi = weights[i - 1], values[i - 1]
            if wi > w:
                dp[i][w] = dp[i - 1][w]
                dec = "skip: item too heavy for capacity"
            else:
                skip = dp[i - 1][w]
                take = dp[i - 1][w - wi] + vi
                if take >= skip:
                    dp[i][w] = take
                    dec = f"take item {i - 1}: {take} >= skip {skip}"
                else:
                    dp[i][w] = skip
                    dec = f"skip item {i - 1}: {skip} > take {take}"
            yield {
                "table": _copy_table_2d(dp),
                "current_cell": (i, w),
                "filling_value": dp[i][w],
                "decision": dec,
                "step": step,
            }
    w = capacity
    picked: List[int] = []
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            picked.append(i - 1)
            w -= weights[i - 1]
    picked.reverse()
    yield {
        "done": True,
        "table": _copy_table_2d(dp),
        "solution": dp[n][capacity],
        "path": picked,
    }


def knapsack_01_plain(weights: List[int], values: List[int], capacity: int) -> int:
    n = len(weights)
    dp = [0] * (capacity + 1)
    for i in range(n):
        wi, vi = weights[i], values[i]
        for w in range(capacity, wi - 1, -1):
            dp[w] = max(dp[w], dp[w - wi] + vi)
    return dp[capacity]


def lcs_traced(str1: str, str2: str) -> Generator[TraceYield, None, None]:
    m, n = len(str1), len(str2)
    dp: List[List[int]] = [[0] * (n + 1) for _ in range(m + 1)]
    step = 0
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            step += 1
            if str1[i - 1] == str2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
                dec = "match: extend LCS by 1"
            elif dp[i - 1][j] >= dp[i][j - 1]:
                dp[i][j] = dp[i - 1][j]
                dec = "drop char from str1"
            else:
                dp[i][j] = dp[i][j - 1]
                dec = "drop char from str2"
            yield {
                "table": _copy_table_2d(dp),
                "current_cell": (i, j),
                "filling_value": dp[i][j],
                "decision": dec,
                "step": step,
            }
    i, j = m, n
    out: List[str] = []
    while i > 0 and j > 0:
        if str1[i - 1] == str2[j - 1]:
            out.append(str1[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] >= dp[i][j - 1]:
            i -= 1
        else:
            j -= 1
    lcs_str = "".join(reversed(out))
    yield {
        "done": True,
        "table": _copy_table_2d(dp),
        "solution": lcs_str,
        "path": list(lcs_str),
    }


def lcs_plain(str1: str, str2: str) -> str:
    m, n = len(str1), len(str2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if str1[i - 1] == str2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    i, j = m, n
    out: List[str] = []
    while i > 0 and j > 0:
        if str1[i - 1] == str2[j - 1]:
            out.append(str1[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] >= dp[i][j - 1]:
            i -= 1
        else:
            j -= 1
    return "".join(reversed(out))


def edit_distance_traced(str1: str, str2: str) -> Generator[TraceYield, None, None]:
    m, n = len(str1), len(str2)
    dp: List[List[int]] = [[0] * (n + 1) for _ in range(m + 1)]
    for j in range(n + 1):
        dp[0][j] = j
    for i in range(m + 1):
        dp[i][0] = i
    step = 0
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            step += 1
            if str1[i - 1] == str2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
                dec = "match: no new operation"
            else:
                del_c = dp[i - 1][j] + 1
                ins_c = dp[i][j - 1] + 1
                sub_c = dp[i - 1][j - 1] + 1
                dp[i][j] = min(del_c, ins_c, sub_c)
                if dp[i][j] == sub_c:
                    dec = "substitute"
                elif dp[i][j] == del_c:
                    dec = "delete from str1"
                else:
                    dec = "insert into str1"
            yield {
                "table": _copy_table_2d(dp),
                "current_cell": (i, j),
                "filling_value": dp[i][j],
                "decision": dec,
                "step": step,
            }
    ops: List[str] = []
    i, j = m, n
    while i > 0 or j > 0:
        if i > 0 and j > 0 and str1[i - 1] == str2[j - 1]:
            ops.append("M")
            i -= 1
            j -= 1
        elif j > 0 and (i == 0 or dp[i][j - 1] + 1 == dp[i][j]):
            ops.append("I")
            j -= 1
        elif i > 0 and (j == 0 or dp[i - 1][j] + 1 == dp[i][j]):
            ops.append("D")
            i -= 1
        else:
            ops.append("S")
            i -= 1
            j -= 1
    ops.reverse()
    yield {
        "done": True,
        "table": _copy_table_2d(dp),
        "solution": dp[m][n],
        "path": ops,
    }


def edit_distance_plain(str1: str, str2: str) -> int:
    m, n = len(str1), len(str2)
    prev = list(range(n + 1))
    for i in range(1, m + 1):
        cur = [i] + [0] * n
        for j in range(1, n + 1):
            if str1[i - 1] == str2[j - 1]:
                cur[j] = prev[j - 1]
            else:
                cur[j] = 1 + min(prev[j], cur[j - 1], prev[j - 1])
        prev = cur
    return prev[n]


def coin_change_traced(coins: List[int], amount: int) -> Generator[TraceYield, None, None]:
    INF = amount + 1
    dp: List[int] = [INF] * (amount + 1)
    dp[0] = 0
    choice: List[Optional[int]] = [None] * (amount + 1)
    if amount == 0:
        yield {
            "done": True,
            "table": _copy_table_1d(dp),
            "solution": 0,
            "path": [],
        }
        return
    step = 0
    for a in range(1, amount + 1):
        step += 1
        best = INF
        best_c: Optional[int] = None
        for c in coins:
            if c <= a and dp[a - c] + 1 < best:
                best = dp[a - c] + 1
                best_c = c
        if best < INF:
            dp[a] = best
            choice[a] = best_c
            dec = f"use coin {best_c}, remainder {a - best_c}"
        else:
            dp[a] = INF
            dec = "unreachable with given coins"
        yield {
            "table": _copy_table_1d(dp),
            "current_cell": a,
            "filling_value": dp[a] if dp[a] < INF else None,
            "decision": dec,
            "step": step,
        }
    if dp[amount] >= INF:
        yield {
            "done": True,
            "table": _copy_table_1d(dp),
            "solution": None,
            "path": [],
        }
        return
    seq: List[int] = []
    a = amount
    while a > 0 and choice[a] is not None:
        seq.append(choice[a])  # type: ignore[arg-type]
        a -= choice[a]  # type: ignore[operator]
    seq.reverse()
    yield {
        "done": True,
        "table": _copy_table_1d(dp),
        "solution": dp[amount],
        "path": seq,
    }


def coin_change_plain(coins: List[int], amount: int) -> int:
    if amount == 0:
        return 0
    INF = amount + 1
    dp = [INF] * (amount + 1)
    dp[0] = 0
    for a in range(1, amount + 1):
        for c in coins:
            if c <= a:
                dp[a] = min(dp[a], dp[a - c] + 1)
    return -1 if dp[amount] >= INF else dp[amount]


def matrix_chain_traced(dimensions: List[int]) -> Generator[TraceYield, None, None]:
    n = len(dimensions) - 1
    if n <= 0:
        yield {
            "done": True,
            "table": [[0]],
            "solution": 0,
            "path": [],
        }
        return
    dp: List[List[int]] = [[0] * n for _ in range(n)]
    split: List[List[Optional[int]]] = [[None] * n for _ in range(n)]
    step = 0
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            step += 1
            best = 2**30
            best_k: Optional[int] = None
            for k in range(i, j):
                cost = (
                    dp[i][k]
                    + dp[k + 1][j]
                    + dimensions[i] * dimensions[k + 1] * dimensions[j + 1]
                )
                if cost < best:
                    best = cost
                    best_k = k
            dp[i][j] = best
            split[i][j] = best_k
            yield {
                "table": _copy_table_2d(dp),
                "current_cell": (i, j),
                "filling_value": best,
                "decision": f"split at k={best_k}",
                "step": step,
            }

    def paren(i: int, j: int) -> str:
        if i == j:
            return f"A{i}"
        k = split[i][j]
        assert k is not None
        return f"({paren(i, k)}{paren(k + 1, j)})"

    expr = paren(0, n - 1) if n else ""
    yield {
        "done": True,
        "table": _copy_table_2d(dp),
        "solution": dp[0][n - 1],
        "path": expr,
    }


def matrix_chain_plain(dimensions: List[int]) -> int:
    n = len(dimensions) - 1
    if n <= 0:
        return 0
    dp = [[0] * n for _ in range(n)]
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            dp[i][j] = min(
                dp[i][k]
                + dp[k + 1][j]
                + dimensions[i] * dimensions[k + 1] * dimensions[j + 1]
                for k in range(i, j)
            )
    return dp[0][n - 1]


def lis_traced(sequence: List[int]) -> Generator[TraceYield, None, None]:
    n = len(sequence)
    if n == 0:
        yield {"done": True, "table": [], "solution": [], "path": []}
        return
    dp: List[int] = [1] * n
    prev: List[Optional[int]] = [None] * n
    step = 0
    for i in range(n):
        for j in range(i):
            step += 1
            if sequence[j] < sequence[i] and dp[j] + 1 > dp[i]:
                dp[i] = dp[j] + 1
                prev[i] = j
                dec = f"extend from index {j}, new_len={dp[i]}"
            else:
                dec = f"skip j={j} (not improving)"
            yield {
                "table": _copy_table_1d(dp),
                "current_cell": i,
                "filling_value": dp[i],
                "decision": dec,
                "step": step,
            }
        step += 1
        yield {
            "table": _copy_table_1d(dp),
            "current_cell": i,
            "filling_value": dp[i],
            "decision": f"finished row i={i}, best ending here={dp[i]}",
            "step": step,
        }
    end = max(range(n), key=lambda x: dp[x])
    lis_seq: List[int] = []
    idx_path: List[int] = []
    cur: Optional[int] = end
    while cur is not None:
        lis_seq.append(sequence[cur])
        idx_path.append(cur)
        cur = prev[cur]
    lis_seq.reverse()
    idx_path.reverse()
    yield {
        "done": True,
        "table": _copy_table_1d(dp),
        "solution": lis_seq,
        "path": idx_path,
    }


def lis_plain(sequence: List[int]) -> List[int]:
    n = len(sequence)
    if n == 0:
        return []
    dp = [1] * n
    prev = [None] * n
    for i in range(n):
        for j in range(i):
            if sequence[j] < sequence[i] and dp[j] + 1 > dp[i]:
                dp[i] = dp[j] + 1
                prev[i] = j
    end = max(range(n), key=lambda x: dp[x])
    out: List[int] = []
    cur: Optional[int] = end
    while cur is not None:
        out.append(sequence[cur])
        cur = prev[cur]
    out.reverse()
    return out


ALGORITHMS: Dict[str, AlgorithmEntry] = {
    "knapsack_01": {
        "traced": knapsack_01_traced,
        "plain": knapsack_01_plain,
        "time": "O(n * capacity)",
        "space": "O(n * capacity) traced table; O(capacity) plain",
        "description": "0/1 knapsack: maximize value under weight capacity.",
    },
    "lcs": {
        "traced": lcs_traced,
        "plain": lcs_plain,
        "time": "O(m * n)",
        "space": "O(m * n)",
        "description": "Longest common subsequence of two strings.",
    },
    "edit_distance": {
        "traced": edit_distance_traced,
        "plain": edit_distance_plain,
        "time": "O(m * n)",
        "space": "O(m * n) traced; O(n) plain",
        "description": "Levenshtein edit distance (insert/delete/substitute).",
    },
    "coin_change": {
        "traced": coin_change_traced,
        "plain": coin_change_plain,
        "time": "O(amount * len(coins))",
        "space": "O(amount)",
        "description": "Minimum coins to make amount; plain returns -1 if impossible.",
    },
    "matrix_chain": {
        "traced": matrix_chain_traced,
        "plain": matrix_chain_plain,
        "time": "O(n^3)",
        "space": "O(n^2)",
        "description": "Optimal parenthesization for matrix chain multiplication costs.",
    },
    "lis": {
        "traced": lis_traced,
        "plain": lis_plain,
        "time": "O(n^2)",
        "space": "O(n)",
        "description": "Longest strictly increasing subsequence (O(n^2) DP for tracing).",
    },
}
