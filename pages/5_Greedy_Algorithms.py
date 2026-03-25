import streamlit as st
import plotly.graph_objects as go

from algorithms.greedy import ALGORITHMS
from core.tracer import collect_steps, get_step

st.set_page_config(page_title="Greedy Algorithms", layout="wide")
st.title("Greedy Algorithms")
st.markdown("Watch greedy choices being made step-by-step")

col_cfg, col_viz = st.columns([1, 3])

with col_cfg:
    algo_name = st.selectbox("Algorithm", list(ALGORITHMS.keys()), format_func=lambda x: x.replace("_", " ").title())
    meta = ALGORITHMS[algo_name]
    st.markdown(f"**Time:** `{meta['time']}`  |  **Space:** `{meta['space']}`")
    st.markdown(f"*{meta['description']}*")

    if algo_name == "activity_selection":
        starts_str = st.text_input("Start times", "1, 3, 0, 5, 8, 5")
        finishes_str = st.text_input("Finish times", "2, 4, 6, 7, 9, 9")
        params = lambda: {
            "starts": [int(x.strip()) for x in starts_str.split(",")],
            "finishes": [int(x.strip()) for x in finishes_str.split(",")],
        }
    elif algo_name == "fractional_knapsack":
        weights_str = st.text_input("Weights", "10, 20, 30")
        values_str = st.text_input("Values", "60, 100, 120")
        capacity = st.number_input("Capacity", 1, 1000, 50)
        params = lambda: {
            "weights": [float(x.strip()) for x in weights_str.split(",")],
            "values": [float(x.strip()) for x in values_str.split(",")],
            "capacity": float(capacity),
        }
    elif algo_name == "huffman":
        chars_str = st.text_input("Characters", "a, b, c, d, e, f")
        freqs_str = st.text_input("Frequencies", "5, 9, 12, 13, 16, 45")
        params = lambda: {
            "chars": [x.strip() for x in chars_str.split(",")],
            "freqs": [int(x.strip()) for x in freqs_str.split(",")],
        }
    else:
        params = lambda: {}

    if st.button("Run Greedy", type="primary"):
        try:
            p = params()
            steps = collect_steps(meta["traced"](**p))
            st.session_state["greedy_steps"] = steps
        except Exception as e:
            st.error(f"Error: {e}")

with col_viz:
    if "greedy_steps" in st.session_state:
        steps = st.session_state["greedy_steps"]
        total = len(steps)
        step_idx = st.slider("Step", 0, max(total - 1, 0), 0, key="greedy_slider")
        current = get_step(steps, step_idx)

        st.markdown(f"### Step {step_idx + 1} / {total}")

        if algo_name == "activity_selection":
            selected = current.get("selected", [])
            curr = current.get("current")
            decision = current.get("decision", "")

            if selected:
                fig = go.Figure()
                for i, (s, f) in enumerate(selected):
                    fig.add_trace(go.Bar(x=[f - s], y=[f"Activity {i}"], base=[s], orientation="h", marker_color="#2ecc71", name=f"({s},{f})"))
                if curr:
                    cs, cf = curr
                    color = "#f39c12" if "reject" in decision else "#3498db"
                    fig.add_trace(go.Bar(x=[cf - cs], y=["Current"], base=[cs], orientation="h", marker_color=color, name=f"({cs},{cf})"))
                fig.update_layout(title="Activity Timeline", xaxis_title="Time", template="plotly_white", showlegend=False, height=300)
                st.plotly_chart(fig, use_container_width=True)

            st.info(f"**Decision:** {decision}")
            st.metric("Selected Activities", len(selected))

        elif algo_name == "fractional_knapsack":
            items = current.get("items_taken", [])
            remaining = current.get("remaining_capacity", 0)
            total_val = current.get("total_value", 0)

            st.metric("Total Value", f"{total_val:.2f}")
            st.metric("Remaining Capacity", f"{remaining:.2f}")
            if items:
                st.markdown("**Items Taken:**")
                for w, v, frac in items:
                    st.markdown(f"- Weight={w}, Value={v}, Fraction={frac:.2f}")

        elif algo_name == "huffman":
            codes = current.get("codes", {})
            merged = current.get("merged")
            tree = current.get("tree_nodes", [])

            st.metric("Tree Nodes", len(tree))
            if merged:
                st.info(f"Merged: freq={merged[0].get('freq',0)} + freq={merged[1].get('freq',0)}")
            if codes:
                st.success("**Huffman Codes:**")
                st.json(codes)
    else:
        st.info("Configure and click **Run Greedy** to start.")
