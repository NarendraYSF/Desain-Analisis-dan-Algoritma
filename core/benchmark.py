from __future__ import annotations

import gc
import statistics
import time
import tracemalloc
from collections.abc import Callable
from typing import Any

import pandas as pd


def _run_once(fn: Callable[..., Any], data: Any) -> tuple[float, int]:
    gc.collect()
    tracemalloc.start()
    try:
        t0 = time.perf_counter()
        fn(data)
        elapsed = time.perf_counter() - t0
        _, peak = tracemalloc.get_traced_memory()
        return elapsed, peak
    finally:
        tracemalloc.stop()


def benchmark_algorithm(
    fn: Callable[..., Any],
    data_generator: Callable[[int], Any],
    sizes: list[int],
    runs: int = 3,
) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for size in sizes:
        times: list[float] = []
        peaks: list[int] = []
        for _ in range(runs):
            data = data_generator(size)
            dt, peak = _run_once(fn, data)
            times.append(dt)
            peaks.append(peak)
        rows.append(
            {
                "size": size,
                "time_mean": statistics.mean(times),
                "time_std": statistics.stdev(times) if len(times) > 1 else 0.0,
                "memory_peak": max(peaks),
            }
        )
    return pd.DataFrame(rows)


def compare_algorithms(
    algorithms: dict[str, Callable[..., Any]],
    data_generator: Callable[[int], Any],
    sizes: list[int],
    runs: int = 3,
) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for name, fn in algorithms.items():
        for size in sizes:
            times: list[float] = []
            peaks: list[int] = []
            for _ in range(runs):
                data = data_generator(size)
                dt, peak = _run_once(fn, data)
                times.append(dt)
                peaks.append(peak)
            rows.append(
                {
                    "algorithm": name,
                    "size": size,
                    "time_mean": statistics.mean(times),
                    "time_std": statistics.stdev(times) if len(times) > 1 else 0.0,
                    "memory_peak": max(peaks),
                }
            )
    return pd.DataFrame(rows)
