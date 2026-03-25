from __future__ import annotations

from collections.abc import Iterator
from typing import Any, TypedDict


class NQueensStep(TypedDict):
    board: list[list[int]]
    placing: tuple[int, int] | None
    conflict: bool
    queens_placed: int
    backtracks: int
    step: int


class SudokuStep(TypedDict):
    board: list[list[int]]
    trying: tuple[int, int, int] | None
    valid: bool
    backtracks: int
    step: int


class SubsetSumStep(TypedDict):
    current_subset: list[int]
    remaining: int
    index: int
    decision: str
    backtracks: int
    step: int


def _empty_board(n: int) -> list[list[int]]:
    return [[0] * n for _ in range(n)]


def _clone_board(b: list[list[int]]) -> list[list[int]]:
    return [list(row) for row in b]


def _nqueens_conflict(board: list[list[int]], row: int, col: int) -> bool:
    n = len(board)
    for c in range(col):
        if board[row][c] == 1:
            return True
    r, c = row - 1, col - 1
    while r >= 0 and c >= 0:
        if board[r][c] == 1:
            return True
        r -= 1
        c -= 1
    r, c = row + 1, col - 1
    while r < n and c >= 0:
        if board[r][c] == 1:
            return True
        r += 1
        c -= 1
    return False


def _queens_placed(board: list[list[int]]) -> int:
    return sum(sum(row) for row in board)


def n_queens_traced(n: int) -> Iterator[NQueensStep]:
    step = 0
    backtracks = 0
    board = _empty_board(n)
    if n == 0:
        yield {
            "board": board,
            "placing": None,
            "conflict": False,
            "queens_placed": 0,
            "backtracks": backtracks,
            "step": step,
        }
        return

    def backtrack(col: int) -> Iterator[NQueensStep]:
        nonlocal step, backtracks
        if col == n:
            step += 1
            yield {
                "board": _clone_board(board),
                "placing": None,
                "conflict": False,
                "queens_placed": _queens_placed(board),
                "backtracks": backtracks,
                "step": step,
            }
            return True
        for row in range(n):
            step += 1
            cf = _nqueens_conflict(board, row, col)
            yield {
                "board": _clone_board(board),
                "placing": (row, col),
                "conflict": cf,
                "queens_placed": _queens_placed(board),
                "backtracks": backtracks,
                "step": step,
            }
            if cf:
                continue
            board[row][col] = 1
            step += 1
            yield {
                "board": _clone_board(board),
                "placing": (row, col),
                "conflict": False,
                "queens_placed": _queens_placed(board),
                "backtracks": backtracks,
                "step": step,
            }
            sub = backtrack(col + 1)
            ok = False
            while True:
                try:
                    yield next(sub)
                except StopIteration as e:
                    ok = bool(e.value)
                    break
            if ok:
                return True
            board[row][col] = 0
            backtracks += 1
            step += 1
            yield {
                "board": _clone_board(board),
                "placing": (row, col),
                "conflict": False,
                "queens_placed": _queens_placed(board),
                "backtracks": backtracks,
                "step": step,
            }
        return False

    root = backtrack(0)
    while True:
        try:
            yield next(root)
        except StopIteration:
            break


def n_queens_plain(n: int) -> list[list[int]] | None:
    board = _empty_board(n)

    def conflict(row: int, col: int) -> bool:
        for c in range(col):
            if board[row][c] == 1:
                return True
        r, c = row - 1, col - 1
        while r >= 0 and c >= 0:
            if board[r][c] == 1:
                return True
            r -= 1
            c -= 1
        r, c = row + 1, col - 1
        while r < n and c >= 0:
            if board[r][c] == 1:
                return True
            r += 1
            c -= 1
        return False

    def solve(col: int) -> bool:
        if col == n:
            return True
        for row in range(n):
            if conflict(row, col):
                continue
            board[row][col] = 1
            if solve(col + 1):
                return True
            board[row][col] = 0
        return False

    if n == 0:
        return board
    if solve(0):
        return board
    return None


def _sudoku_valid(board: list[list[int]], row: int, col: int, val: int) -> bool:
    for c in range(9):
        if c != col and board[row][c] == val:
            return False
    for r in range(9):
        if r != row and board[r][col] == val:
            return False
    br, bc = 3 * (row // 3), 3 * (col // 3)
    for r in range(br, br + 3):
        for c in range(bc, bc + 3):
            if (r, c) != (row, col) and board[r][c] == val:
                return False
    return True


def sudoku_traced(board: list[list[int]]) -> Iterator[SudokuStep]:
    step = 0
    backtracks = 0
    b = _clone_board(board)
    if any(len(row) != 9 for row in b) or len(b) != 9:
        raise ValueError("board must be 9x9")

    def next_empty() -> tuple[int, int] | None:
        for r in range(9):
            for c in range(9):
                if b[r][c] == 0:
                    return r, c
        return None

    def solve() -> Iterator[SudokuStep]:
        nonlocal step, backtracks
        cell = next_empty()
        if cell is None:
            step += 1
            yield {
                "board": _clone_board(b),
                "trying": None,
                "valid": True,
                "backtracks": backtracks,
                "step": step,
            }
            return True
        row, col = cell
        for val in range(1, 10):
            step += 1
            vok = _sudoku_valid(b, row, col, val)
            yield {
                "board": _clone_board(b),
                "trying": (row, col, val),
                "valid": vok,
                "backtracks": backtracks,
                "step": step,
            }
            if not vok:
                continue
            b[row][col] = val
            sub = solve()
            ok = False
            while True:
                try:
                    yield next(sub)
                except StopIteration as e:
                    ok = bool(e.value)
                    break
            if ok:
                return True
            b[row][col] = 0
            backtracks += 1
            step += 1
            yield {
                "board": _clone_board(b),
                "trying": (row, col, val),
                "valid": True,
                "backtracks": backtracks,
                "step": step,
            }
        return False

    root = solve()
    while True:
        try:
            yield next(root)
        except StopIteration:
            break


def sudoku_plain(board: list[list[int]]) -> list[list[int]] | None:
    b = _clone_board(board)
    if any(len(row) != 9 for row in b) or len(b) != 9:
        raise ValueError("board must be 9x9")

    def next_empty() -> tuple[int, int] | None:
        for r in range(9):
            for c in range(9):
                if b[r][c] == 0:
                    return r, c
        return None

    def solve() -> bool:
        cell = next_empty()
        if cell is None:
            return True
        row, col = cell
        for val in range(1, 10):
            if not _sudoku_valid(b, row, col, val):
                continue
            b[row][col] = val
            if solve():
                return True
            b[row][col] = 0
        return False

    if solve():
        return b
    return None


def subset_sum_traced(nums: list[int], target: int) -> Iterator[SubsetSumStep]:
    step = 0
    backtracks = 0
    current: list[int] = []
    n = len(nums)

    def dfs(i: int, remaining: int) -> Iterator[SubsetSumStep]:
        nonlocal step, backtracks
        if remaining == 0:
            step += 1
            yield {
                "current_subset": list(current),
                "remaining": remaining,
                "index": i,
                "decision": "found",
                "backtracks": backtracks,
                "step": step,
            }
            return True
        if i == n or remaining < 0:
            step += 1
            yield {
                "current_subset": list(current),
                "remaining": remaining,
                "index": i,
                "decision": "reject",
                "backtracks": backtracks,
                "step": step,
            }
            return False
        step += 1
        yield {
            "current_subset": list(current),
            "remaining": remaining,
            "index": i,
            "decision": "try_include",
            "backtracks": backtracks,
            "step": step,
        }
        current.append(nums[i])
        sub_inc = dfs(i + 1, remaining - nums[i])
        inc_ok = False
        while True:
            try:
                yield next(sub_inc)
            except StopIteration as e:
                inc_ok = bool(e.value)
                break
        current.pop()
        if inc_ok:
            return True
        step += 1
        yield {
            "current_subset": list(current),
            "remaining": remaining,
            "index": i,
            "decision": "try_exclude",
            "backtracks": backtracks,
            "step": step,
        }
        sub_exc = dfs(i + 1, remaining)
        exc_ok = False
        while True:
            try:
                yield next(sub_exc)
            except StopIteration as e:
                exc_ok = bool(e.value)
                break
        if exc_ok:
            return True
        backtracks += 1
        step += 1
        yield {
            "current_subset": list(current),
            "remaining": remaining,
            "index": i,
            "decision": "backtrack",
            "backtracks": backtracks,
            "step": step,
        }
        return False

    root = dfs(0, target)
    while True:
        try:
            yield next(root)
        except StopIteration:
            break


def subset_sum_plain(nums: list[int], target: int) -> list[int] | None:
    n = len(nums)
    res: list[int] = []

    def dfs(i: int, rem: int) -> bool:
        if rem == 0:
            return True
        if i == n or rem < 0:
            return False
        res.append(nums[i])
        if dfs(i + 1, rem - nums[i]):
            return True
        res.pop()
        if dfs(i + 1, rem):
            return True
        return False

    if dfs(0, target):
        return res
    return None


ALGORITHMS: dict[str, dict[str, Any]] = {
    "n_queens": {
        "traced": n_queens_traced,
        "plain": n_queens_plain,
        "time": "O(n!)",
        "space": "O(n)",
        "description": "Place n queens on an n×n board with no attacks.",
    },
    "sudoku": {
        "traced": sudoku_traced,
        "plain": sudoku_plain,
        "time": "O(9^m)",
        "space": "O(1)",
        "description": "Isi Sudoku 9×9 dengan backtracking.",
    },
    "subset_sum": {
        "traced": subset_sum_traced,
        "plain": subset_sum_plain,
        "time": "O(2^n)",
        "space": "O(n)",
        "description": "Find a subset whose sum equals the target.",
    },
}
