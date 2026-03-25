from __future__ import annotations

from typing import Any, Iterable, Sequence

import numpy as np
import pandas as pd
import plotly.graph_objects as go


def _index_set(x: Iterable[int] | None) -> set[int]:
    return set(x) if x is not None else set()


def create_bar_chart(
    array: Sequence[float | int],
    comparing: Iterable[int] | None = None,
    swapped: Iterable[int] | None = None,
    sorted_indices: Iterable[int] | None = None,
    title: str = "",
) -> go.Figure:
    n = len(array)
    x = list(range(n))
    cmp_s = _index_set(comparing)
    swp_s = _index_set(swapped)
    sort_s = _index_set(sorted_indices)
    colors: list[str] = []
    for i in range(n):
        if i in sort_s:
            colors.append("#2ecc71")
        elif i in swp_s:
            colors.append("#e74c3c")
        elif i in cmp_s:
            colors.append("#f39c12")
        else:
            colors.append("#3498db")
    fig = go.Figure(
        data=[
            go.Bar(
                x=x,
                y=list(array),
                marker=dict(color=colors, line=dict(color="#2c3e50", width=1)),
            )
        ]
    )
    fig.update_layout(
        title=dict(text=title, font=dict(size=18)),
        xaxis_title="Index",
        yaxis_title="Value",
        template="plotly_white",
        margin=dict(l=50, r=30, t=60, b=50),
        showlegend=False,
    )
    return fig


def _iter_edges(graph_dict: dict[Any, Any]) -> list[tuple[Any, Any, float | None]]:
    edges: list[tuple[Any, Any, float | None]] = []
    seen: set[tuple[Any, Any]] = set()
    for u, nbrs in graph_dict.items():
        if isinstance(nbrs, dict):
            for v, w in nbrs.items():
                a, b = (u, v) if u <= v else (v, u)
                if (a, b) not in seen:
                    seen.add((a, b))
                    edges.append((u, v, float(w)))
        else:
            for v in nbrs:
                a, b = (u, v) if u <= v else (v, u)
                if (a, b) not in seen:
                    seen.add((a, b))
                    edges.append((u, v, None))
    return edges


def create_graph_figure(
    graph_dict: dict[Any, Any],
    pos: dict[Any, tuple[float, float]],
    visited: Iterable[Any] | None = None,
    current: Any | None = None,
    path_edges: Iterable[tuple[Any, Any]] | None = None,
    mst_edges: Iterable[tuple[Any, Any]] | None = None,
    title: str = "",
) -> go.Figure:
    fig = go.Figure()
    visited_s = set(visited) if visited is not None else set()
    path_set = {tuple(sorted((a, b))) for a, b in (path_edges or [])}
    mst_set = {tuple(sorted((a, b))) for a, b in (mst_edges or [])}

    for u, v, _w in _iter_edges(graph_dict):
        if u not in pos or v not in pos:
            continue
        x0, y0 = pos[u]
        x1, y1 = pos[v]
        key = tuple(sorted((u, v)))
        line_color = "#bdc3c7"
        line_width = 2
        if key in mst_set:
            line_color = "#9b59b6"
            line_width = 4
        if key in path_set:
            line_color = "#e67e22"
            line_width = 4
        fig.add_trace(
            go.Scatter(
                x=[x0, x1, None],
                y=[y0, y1, None],
                mode="lines",
                line=dict(color=line_color, width=line_width),
                hoverinfo="skip",
                showlegend=False,
            )
        )

    nodes = list(pos.keys())
    xs = [pos[n][0] for n in nodes]
    ys = [pos[n][1] for n in nodes]
    node_colors: list[str] = []
    for n in nodes:
        if current is not None and n == current:
            node_colors.append("#e74c3c")
        elif n in visited_s:
            node_colors.append("#3498db")
        else:
            node_colors.append("#ecf0f1")
    fig.add_trace(
        go.Scatter(
            x=xs,
            y=ys,
            mode="markers+text",
            text=[str(n) for n in nodes],
            textposition="top center",
            marker=dict(size=22, color=node_colors, line=dict(color="#2c3e50", width=2)),
            hovertext=[str(n) for n in nodes],
            hoverinfo="text",
            showlegend=False,
        )
    )
    fig.update_layout(
        title=dict(text=title, font=dict(size=18)),
        template="plotly_white",
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        margin=dict(l=20, r=20, t=60, b=20),
        plot_bgcolor="#fafafa",
    )
    return fig


def create_heatmap(
    table: Sequence[Sequence[float | int | None]],
    current_cell: tuple[int, int] | None = None,
    title: str = "",
) -> go.Figure:
    z = [[(0.0 if c is None else float(c)) for c in row] for row in table]
    fig = go.Figure(
        data=go.Heatmap(
            z=z,
            colorscale="Blues",
            showscale=True,
            hoverongaps=False,
        )
    )
    if current_cell is not None:
        r, c = current_cell
        if 0 <= r < len(z) and 0 <= c < len(z[r]):
            fig.add_trace(
                go.Scatter(
                    x=[c],
                    y=[r],
                    mode="markers",
                    marker=dict(
                        symbol="square",
                        size=28,
                        color="rgba(231,76,60,0.35)",
                        line=dict(color="#e74c3c", width=3),
                    ),
                    showlegend=False,
                    hoverinfo="skip",
                )
            )
    fig.update_layout(
        title=dict(text=title, font=dict(size=18)),
        template="plotly_white",
        yaxis=dict(autorange="reversed"),
        margin=dict(l=60, r=30, t=60, b=50),
    )
    return fig


def create_board(
    board: Sequence[Sequence[Any]],
    highlights: Iterable[tuple[int, int]] | None = None,
    title: str = "",
) -> go.Figure:
    rows = len(board)
    cols = len(board[0]) if rows else 0
    hl = set(highlights or [])
    z = np.zeros((rows, cols))
    annotations: list[dict[str, Any]] = []
    for i in range(rows):
        for j in range(cols):
            val = board[i][j]
            text = "" if val is None or val == 0 else str(val)
            bg = "#f8f9fa"
            if (i, j) in hl:
                bg = "#ffeaa7"
            annotations.append(
                dict(
                    x=j,
                    y=i,
                    text=text,
                    showarrow=False,
                    font=dict(size=16, color="#2c3e50"),
                    xref="x",
                    yref="y",
                )
            )
    fig = go.Figure(
        data=go.Heatmap(
            z=z,
            colorscale=[[0, "#ffffff"], [1, "#ffffff"]],
            showscale=False,
            hoverinfo="skip",
        )
    )
    fig.update_traces(opacity=0)
    for ann in annotations:
        fig.add_annotation(**ann)
    shapes: list[dict[str, Any]] = []
    for i in range(rows + 1):
        shapes.append(
            dict(
                type="line",
                x0=-0.5,
                x1=cols - 0.5,
                y0=i - 0.5,
                y1=i - 0.5,
                line=dict(color="#2c3e50", width=2),
            )
        )
    for j in range(cols + 1):
        shapes.append(
            dict(
                type="line",
                x0=j - 0.5,
                x1=j - 0.5,
                y0=-0.5,
                y1=rows - 0.5,
                line=dict(color="#2c3e50", width=2),
            )
        )
    for i, j in hl:
        shapes.append(
            dict(
                type="rect",
                x0=j - 0.5,
                x1=j + 0.5,
                y0=i - 0.5,
                y1=i + 0.5,
                fillcolor="rgba(243,156,18,0.35)",
                line=dict(color="#f39c12", width=2),
            )
        )
    fig.update_layout(
        title=dict(text=title, font=dict(size=18)),
        shapes=shapes,
        template="plotly_white",
        xaxis=dict(
            range=[-0.5, cols - 0.5],
            showgrid=False,
            zeroline=False,
            showticklabels=False,
        ),
        yaxis=dict(
            range=[rows - 0.5, -0.5],
            showgrid=False,
            zeroline=False,
            showticklabels=False,
        ),
        margin=dict(l=30, r=30, t=60, b=30),
        plot_bgcolor="#ecf0f1",
    )
    return fig


def create_benchmark_chart(df: pd.DataFrame, title: str = "") -> go.Figure:
    fig = go.Figure()
    if "algorithm" in df.columns:
        for algo in df["algorithm"].unique():
            sub = df[df["algorithm"] == algo].sort_values("size")
            fig.add_trace(
                go.Scatter(
                    x=sub["size"],
                    y=sub["time_mean"],
                    mode="lines+markers",
                    name=str(algo),
                    error_y=dict(type="data", array=sub["time_std"], visible=True),
                    line=dict(width=3),
                )
            )
        fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02))
    else:
        sub = df.sort_values("size")
        fig.add_trace(
            go.Scatter(
                x=sub["size"],
                y=sub["time_mean"],
                mode="lines+markers",
                name="time",
                error_y=dict(type="data", array=sub["time_std"], visible=True),
                line=dict(color="#2980b9", width=3),
                marker=dict(size=10),
            )
        )
    fig.update_layout(
        title=dict(text=title, font=dict(size=18)),
        xaxis_title="Input size (n)",
        yaxis_title="Time (s)",
        template="plotly_white",
        margin=dict(l=60, r=30, t=80, b=60),
    )
    return fig


def create_complexity_chart(
    sizes: Sequence[int | float],
    times: Sequence[float],
    fitted_curves: dict[str, Sequence[float]],
    best_fit: str,
    title: str = "",
) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=list(sizes),
            y=list(times),
            mode="markers",
            name="Empirical",
            marker=dict(size=12, color="#e74c3c", line=dict(color="#c0392b", width=1)),
        )
    )
    palette = [
        "#3498db",
        "#9b59b6",
        "#1abc9c",
        "#f39c12",
        "#34495e",
        "#e91e63",
        "#00bcd4",
    ]
    for i, (name, curve) in enumerate(fitted_curves.items()):
        color = palette[i % len(palette)]
        width = 4 if name == best_fit else 1.5
        dash = "solid" if name == best_fit else "dot"
        fig.add_trace(
            go.Scatter(
                x=list(sizes),
                y=list(curve),
                mode="lines",
                name=name + (" ★" if name == best_fit else ""),
                line=dict(color=color, width=width, dash=dash),
            )
        )
    fig.update_layout(
        title=dict(text=title, font=dict(size=18)),
        xaxis_title="n",
        yaxis_title="Time (s)",
        template="plotly_white",
        legend=dict(orientation="v", yanchor="top", y=1),
        margin=dict(l=60, r=30, t=60, b=60),
    )
    return fig
