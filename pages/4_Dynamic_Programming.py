import streamlit as st

from algorithms.dynamic_programming import ALGORITHMS
from core.tracer import collect_steps, get_step
from core.visualizer import create_heatmap

st.set_page_config(page_title="Dynamic Programming", layout="wide")
st.title("Dynamic Programming")
st.markdown("Watch DP tables fill step-by-step")

col_cfg, col_viz = st.columns([1, 3])

with col_cfg:
    algo_name = st.selectbox("Problem", list(ALGORITHMS.keys()), format_func=lambda x: x.replace("_", " ").title())
    meta = ALGORITHMS[algo_name]
    st.markdown(f"**Time:** `{meta['time']}`  |  **Space:** `{meta['space']}`")
    st.markdown(f"*{meta['description']}*")

    if algo_name == "knapsack_01":
        weights_str = st.text_input("Weights", "2, 3, 4, 5")
        values_str = st.text_input("Values", "3, 4, 5, 6")
        capacity = st.number_input("Capacity", 1, 100, 8)
        params = lambda: {
            "weights": [int(x.strip()) for x in weights_str.split(",")],
            "values": [int(x.strip()) for x in values_str.split(",")],
            "capacity": capacity,
        }
    elif algo_name == "lcs":
        s1 = st.text_input("String 1", "ABCBDAB")
        s2 = st.text_input("String 2", "BDCAB")
        params = lambda: {"str1": s1, "str2": s2}
    elif algo_name == "edit_distance":
        s1 = st.text_input("String 1", "kitten")
        s2 = st.text_input("String 2", "sitting")
        params = lambda: {"str1": s1, "str2": s2}
    elif algo_name == "coin_change":
        coins_str = st.text_input("Coins", "1, 5, 10, 25")
        amount = st.number_input("Amount", 1, 1000, 30)
        params = lambda: {
            "coins": [int(x.strip()) for x in coins_str.split(",")],
            "amount": amount,
        }
    elif algo_name == "matrix_chain":
        dims_str = st.text_input("Dimensions (n+1 values for n matrices)", "30, 35, 15, 5, 10, 20, 25")
        params = lambda: {"dimensions": [int(x.strip()) for x in dims_str.split(",")]}
    elif algo_name == "lis":
        seq_str = st.text_input("Sequence", "10, 9, 2, 5, 3, 7, 101, 18")
        params = lambda: {"sequence": [int(x.strip()) for x in seq_str.split(",")]}
    else:
        params = lambda: {}

    if st.button("Run DP", type="primary"):
        try:
            p = params()
            steps = collect_steps(meta["traced"](**p))
            st.session_state["dp_steps"] = steps
            st.session_state["dp_idx"] = 0
        except Exception as e:
            st.error(f"Error: {e}")

with col_viz:
    if "dp_steps" in st.session_state:
        steps = st.session_state["dp_steps"]
        total = len(steps)
        step_idx = st.slider("Step", 0, max(total - 1, 0), 0, key="dp_slider")
        current = get_step(steps, step_idx)

        table = current.get("table", [])
        cell = current.get("current_cell")
        decision = current.get("decision", "")
        done = current.get("done", False)

        if table and isinstance(table[0], list):
            fig = create_heatmap(table, current_cell=cell, title=f"DP Table — Step {step_idx + 1}/{total}")
            st.plotly_chart(fig, use_container_width=True)
        elif table:
            fig = create_heatmap([table], current_cell=(0, cell) if isinstance(cell, int) else cell, title=f"DP Array — Step {step_idx + 1}/{total}")
            st.plotly_chart(fig, use_container_width=True)

        mc1, mc2 = st.columns(2)
        mc1.metric("Step", f"{step_idx + 1}/{total}")
        filling = current.get("filling_value", "—")
        mc2.metric("Value", filling)

        if decision:
            st.info(f"**Decision:** {decision}")

        if done:
            st.success(f"**Optimal Solution:** {current.get('solution', 'N/A')}")
            path = current.get("path")
            if path:
                st.markdown(f"**Path/Items:** `{path}`")
    else:
        st.info("Configure parameters and click **Run DP** to start.")
