import streamlit as st
import plotly.graph_objects as go

from algorithms.divide_conquer import ALGORITHMS
from core.tracer import collect_steps, get_step
from core.visualizer import create_bar_chart
from utils.data_generator import random_array, random_points

st.set_page_config(page_title="Divide & Conquer", layout="wide")
st.title("Divide & Conquer")
st.markdown("Visualize recursive decomposition and combination")

col_cfg, col_viz = st.columns([1, 3])

with col_cfg:
    algo_name = st.selectbox("Algorithm", list(ALGORITHMS.keys()), format_func=lambda x: x.replace("_", " ").title())
    meta = ALGORITHMS[algo_name]
    st.markdown(f"**Time:** `{meta['time']}`  |  **Space:** `{meta['space']}`")

    if algo_name == "merge_sort":
        size = st.slider("Array Size", 4, 30, 10)
        if st.button("Generate & Run", type="primary"):
            arr = random_array(size, 1, 99)
            steps = collect_steps(meta["traced"](arr))
            st.session_state["dc_steps"] = steps
            st.session_state["dc_algo"] = algo_name

    elif algo_name == "closest_pair":
        n_pts = st.slider("Number of Points", 4, 30, 12)
        if st.button("Generate & Run", type="primary"):
            pts = random_points(n_pts)
            steps = collect_steps(meta["traced"](pts))
            st.session_state["dc_steps"] = steps
            st.session_state["dc_algo"] = algo_name
            st.session_state["dc_points"] = pts

    elif algo_name == "karatsuba":
        x = st.number_input("X", value=1234)
        y = st.number_input("Y", value=5678)
        if st.button("Run Karatsuba", type="primary"):
            steps = collect_steps(meta["traced"](int(x), int(y)))
            st.session_state["dc_steps"] = steps
            st.session_state["dc_algo"] = algo_name

with col_viz:
    if "dc_steps" in st.session_state:
        steps = st.session_state["dc_steps"]
        algo = st.session_state["dc_algo"]
        total = len(steps)
        step_idx = st.slider("Step", 0, max(total - 1, 0), 0, key="dc_slider")
        current = get_step(steps, step_idx)

        if algo == "merge_sort":
            arr = current.get("array", [])
            left = current.get("left", [])
            right = current.get("right", [])
            merging = current.get("merging", False)
            depth = current.get("depth", 0)

            fig = create_bar_chart(arr, title=f"Merge Sort — Step {step_idx + 1}/{total} (depth={depth})")
            st.plotly_chart(fig, use_container_width=True)

            mc1, mc2, mc3 = st.columns(3)
            mc1.metric("Phase", "Merging" if merging else "Dividing")
            mc2.metric("Depth", depth)
            mc3.metric("Step", f"{step_idx + 1}/{total}")
            if left or right:
                st.markdown(f"**Left:** `{left}`  |  **Right:** `{right}`")

        elif algo == "closest_pair":
            pts = current.get("points", [])
            strip = current.get("strip", [])
            pair = current.get("closest_pair")
            min_dist = current.get("min_dist", float("inf"))

            fig = go.Figure()
            if pts:
                xs, ys = zip(*pts)
                fig.add_trace(go.Scatter(x=list(xs), y=list(ys), mode="markers", marker=dict(size=10, color="#3498db"), name="Points"))
            if strip:
                sx, sy = zip(*strip)
                fig.add_trace(go.Scatter(x=list(sx), y=list(sy), mode="markers", marker=dict(size=12, color="#f39c12", symbol="diamond"), name="Strip"))
            if pair:
                p1, p2 = pair
                fig.add_trace(go.Scatter(x=[p1[0], p2[0]], y=[p1[1], p2[1]], mode="lines+markers", line=dict(color="#e74c3c", width=3), marker=dict(size=14, color="#e74c3c"), name=f"Closest ({min_dist:.2f})"))
            fig.update_layout(title=f"Closest Pair — Step {step_idx + 1}/{total}", template="plotly_white")
            st.plotly_chart(fig, use_container_width=True)
            st.metric("Min Distance", f"{min_dist:.4f}" if min_dist < float("inf") else "∞")

        elif algo == "karatsuba":
            x_val = current.get("x", 0)
            y_val = current.get("y", 0)
            sub = current.get("sub_products", {})
            result = current.get("result", 0)
            depth = current.get("depth", 0)

            st.markdown(f"### Step {step_idx + 1} / {total}")
            mc1, mc2, mc3 = st.columns(3)
            mc1.metric("X", x_val)
            mc2.metric("Y", y_val)
            mc3.metric("Depth", depth)
            st.metric("Result", result)
            if sub:
                st.markdown("**Sub-products:**")
                st.json(sub)
    else:
        st.info("Configure and click **Generate & Run** to start.")
