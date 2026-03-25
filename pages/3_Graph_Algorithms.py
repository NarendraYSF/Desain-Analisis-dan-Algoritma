import streamlit as st
import networkx as nx

from algorithms.graph import ALGORITHMS
from core.tracer import collect_steps, get_step
from core.visualizer import create_graph_figure
from utils.data_generator import random_graph

st.set_page_config(page_title="Graph Algorithms", layout="wide")
st.title("Graph Algorithms")
st.markdown("BFS, DFS, Dijkstra, Bellman-Ford, Prim, Kruskal, Topological Sort")


def _dict_graph_to_tuple_list(g: dict) -> dict:
    """Convert {node: {nbr: weight}} to {node: [(nbr, weight)]}."""
    result = {}
    for u, nbrs in g.items():
        if isinstance(nbrs, dict):
            result[u] = [(v, w) for v, w in nbrs.items()]
        elif isinstance(nbrs, list) and nbrs and isinstance(nbrs[0], tuple):
            result[u] = list(nbrs)
        else:
            result[u] = [(v, 1.0) for v in nbrs]
    return result


col_cfg, col_viz = st.columns([1, 3])

with col_cfg:
    algo_name = st.selectbox("Algorithm", list(ALGORITHMS.keys()), format_func=lambda x: x.replace("_", " ").title())
    meta = ALGORITHMS[algo_name]
    st.markdown(f"**Time:** `{meta['time']}`  |  **Space:** `{meta['space']}`")
    st.markdown(f"*{meta['description']}*")

    n_nodes = st.slider("Nodes", 4, 15, 7)
    n_edges = st.slider("Edges", n_nodes - 1, n_nodes * (n_nodes - 1) // 2, min(n_nodes * 2, n_nodes * (n_nodes - 1) // 2))
    start_node = st.number_input("Start Node", 0, n_nodes - 1, 0)

    if st.button("Generate Graph & Run", type="primary"):
        raw = random_graph(n_nodes, n_edges, weighted=True, directed=False)
        g = _dict_graph_to_tuple_list(raw)
        for i in range(n_nodes):
            if i not in g:
                g[i] = []

        nxg = nx.Graph()
        for u, nbrs in g.items():
            for v, w in nbrs:
                nxg.add_edge(u, v, weight=w)
        for i in range(n_nodes):
            nxg.add_node(i)
        pos = nx.spring_layout(nxg, seed=42)
        pos = {k: (float(v[0]), float(v[1])) for k, v in pos.items()}

        if algo_name in ("bfs", "dfs"):
            steps = collect_steps(meta["traced"](g, start_node))
        elif algo_name in ("dijkstra", "bellman_ford"):
            steps = collect_steps(meta["traced"](g, start_node))
        elif algo_name in ("prim", "kruskal"):
            steps = collect_steps(meta["traced"](g))
        elif algo_name == "topological_sort":
            dag = {}
            for u, nbrs in g.items():
                dag[u] = [(v, w) for v, w in nbrs if v > u]
            steps = collect_steps(meta["traced"](dag))
        else:
            steps = collect_steps(meta["traced"](g, start_node))

        st.session_state["graph_steps"] = steps
        st.session_state["graph_pos"] = pos
        st.session_state["graph_g"] = g

with col_viz:
    if "graph_steps" in st.session_state:
        steps = st.session_state["graph_steps"]
        pos = st.session_state["graph_pos"]
        g = st.session_state["graph_g"]
        total = len(steps)

        step_idx = st.slider("Step", 0, max(total - 1, 0), 0, key="graph_slider")
        current = get_step(steps, step_idx)

        visited = current.get("visited", set())
        curr_node = current.get("current")
        mst_edges_raw = current.get("mst_edges", [])
        edges_explored = current.get("edges_explored", [])

        path_edges = [(u, v) for u, v in edges_explored] if edges_explored else None
        mst_display = [(u, v) for u, v, *_ in mst_edges_raw] if mst_edges_raw else None

        g_for_viz = {}
        for u, nbrs in g.items():
            g_for_viz[u] = {v: w for v, w in nbrs}

        fig = create_graph_figure(
            g_for_viz, pos,
            visited=visited,
            current=curr_node,
            path_edges=path_edges,
            mst_edges=mst_display,
            title=f"{algo_name.replace('_',' ').title()} — Step {step_idx + 1}/{total}",
        )
        st.plotly_chart(fig, use_container_width=True)

        mc1, mc2, mc3 = st.columns(3)
        mc1.metric("Step", f"{step_idx + 1}/{total}")
        mc2.metric("Visited", len(visited) if isinstance(visited, (set, list)) else 0)

        distances = current.get("distances")
        if distances:
            mc3.metric("Distances Found", len([v for v in distances.values() if v < float("inf")]))
        elif mst_edges_raw:
            total_w = current.get("total_weight", sum(e[2] for e in mst_edges_raw if len(e) > 2))
            mc3.metric("MST Weight", f"{total_w:.2f}")
        else:
            mc3.metric("Current Node", curr_node if curr_node is not None else "—")

        if distances:
            st.markdown("**Distances:**")
            st.json({str(k): (f"{v:.2f}" if v < float("inf") else "∞") for k, v in sorted(distances.items())})
    else:
        st.info("Configure and click **Generate Graph & Run** to start.")
