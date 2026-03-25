from __future__ import annotations

import math
from typing import Any, Callable

import numpy as np
from scipy.optimize import curve_fit


def _r_squared(y: np.ndarray, y_pred: np.ndarray) -> float:
    ss_res = float(np.sum((y - y_pred) ** 2))
    ss_tot = float(np.sum((y - np.mean(y)) ** 2))
    if ss_tot <= 0:
        return 1.0 if ss_res <= 0 else 0.0
    return 1.0 - ss_res / ss_tot


def theoretical_curve(complexity: str, sizes: list[int | float]) -> list[float]:
    n = np.asarray(sizes, dtype=float)
    c = complexity.strip()
    if c == "O(1)":
        return [1.0 for _ in sizes]
    if c == "O(log n)":
        return [math.log(max(x, 1e-12)) for x in n]
    if c == "O(n)":
        return [float(x) for x in n]
    if c == "O(n log n)":
        return [float(x * math.log(max(x, 1e-12))) for x in n]
    if c == "O(n²)" or c == "O(n^2)":
        return [float(x * x) for x in n]
    if c == "O(n³)" or c == "O(n^3)":
        return [float(x**3) for x in n]
    if c == "O(2^n)":
        out: list[float] = []
        for x in n:
            if x > 100:
                out.append(float("inf"))
            else:
                out.append(float(2**int(x)))
        return out
    raise ValueError(f"Unknown complexity: {complexity!r}")


def fit_complexity(sizes: list, times: list) -> dict[str, Any]:
    x = np.asarray(sizes, dtype=float)
    y = np.asarray(times, dtype=float)
    if x.size == 0 or y.size == 0 or x.size != y.size:
        return {
            "best_fit": "O(1)",
            "r_squared": 0.0,
            "all_fits": {},
            "fitted_curves": {},
        }

    models: dict[str, tuple[Callable[..., Any], np.ndarray, tuple[float, ...]]] = {}

    def f_const(_x: np.ndarray, a: float) -> np.ndarray:
        return np.full_like(_x, a, dtype=float)

    def f_log(_x: np.ndarray, a: float, b: float) -> np.ndarray:
        return a * np.log(np.maximum(_x, 1e-12)) + b

    def f_lin(_x: np.ndarray, a: float, b: float) -> np.ndarray:
        return a * _x + b

    def f_nlogn(_x: np.ndarray, a: float, b: float) -> np.ndarray:
        return a * _x * np.log(np.maximum(_x, 1e-12)) + b

    def f_quad(_x: np.ndarray, a: float, b: float) -> np.ndarray:
        return a * _x**2 + b

    def f_cub(_x: np.ndarray, a: float, b: float) -> np.ndarray:
        return a * _x**3 + b

    def f_exp(_x: np.ndarray, a: float, b: float) -> np.ndarray:
        cap = np.minimum(_x, 80.0)
        return a * np.exp(cap * np.log(2.0)) + b

    p0_const = (float(np.mean(y)),)
    p0_2p = (1.0, float(np.min(y)))
    p0_exp = (max(float(np.median(y)) / max(2.0 ** float(np.min(x)), 1e-12), 1e-12), 0.0)

    models["O(1)"] = (f_const, x, p0_const)
    models["O(log n)"] = (f_log, x, p0_2p)
    models["O(n)"] = (f_lin, x, p0_2p)
    models["O(n log n)"] = (f_nlogn, x, p0_2p)
    models["O(n²)"] = (f_quad, x, p0_2p)
    models["O(n³)"] = (f_cub, x, p0_2p)
    models["O(2^n)"] = (f_exp, x, p0_exp)

    all_fits: dict[str, float] = {}
    fitted_curves: dict[str, list[float]] = {}
    best_name = "O(1)"
    best_r2 = -float("inf")

    for name, (func, xv, p0) in models.items():
        try:
            popt, _ = curve_fit(func, xv, y, p0=p0, maxfev=20000)
            y_hat = func(xv, *popt)
            if not np.all(np.isfinite(y_hat)):
                all_fits[name] = float("-inf")
                fitted_curves[name] = [float("nan")] * len(sizes)
                continue
            r2 = _r_squared(y, y_hat)
            all_fits[name] = r2
            fitted_curves[name] = [float(v) for v in y_hat]
            if r2 > best_r2:
                best_r2 = r2
                best_name = name
        except (RuntimeError, ValueError):
            all_fits[name] = float("-inf")
            fitted_curves[name] = [float("nan")] * len(sizes)

    if best_r2 == -float("inf"):
        best_name = "O(1)"
        best_r2 = 0.0

    return {
        "best_fit": best_name,
        "r_squared": float(best_r2),
        "all_fits": all_fits,
        "fitted_curves": fitted_curves,
    }
