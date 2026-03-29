import streamlit as st

from algorithms.searching import ALGORITHMS
from core.tracer import collect_steps, get_step
from core.visualizer import create_bar_chart

st.set_page_config(page_title="Searching Algorithms", layout="wide")
st.title("Searching Algorithms")
st.markdown("Visualize search operations step-by-step")

col_cfg, col_viz = st.columns([1, 3])

with col_cfg:
    algo_name = st.selectbox("Algorithm", list(ALGORITHMS.keys()), format_func=lambda x: x.replace("_", " ").title())
    meta = ALGORITHMS[algo_name]
    st.markdown(f"**Best:** `{meta['time_best']}`  |  **Avg:** `{meta['time_avg']}`  |  **Worst:** `{meta['time_worst']}`")

    arr_input = st.text_input("Array (comma-separated, sorted for binary/interpolation)", "2, 5, 8, 12, 16, 23, 38, 42, 56, 72, 91")
    target = st.number_input("Target Value", value=23)

    if st.button("Search", type="primary"):
        try:
            arr = [int(x.strip()) for x in arr_input.split(",")]
        except ValueError:
            st.error("Invalid array input.")
            arr = []
        if arr:
            steps = collect_steps(meta["traced"](arr, target))
            st.session_state["search_steps"] = steps
            st.session_state["search_idx"] = 0

with col_viz:
    if "search_steps" in st.session_state:
        steps = st.session_state["search_steps"]
        total = len(steps)
        if total > 1:
            step_idx = st.slider("Step", 0, total - 1, 0, key="search_slider")
        else:
            step_idx = 0

        current = get_step(steps, step_idx)
        arr = current.get("array", [])
        checking = current.get("checking")
        low = current.get("low", 0)
        high = current.get("high", len(arr) - 1)
        found = current.get("found")

        highlight_compare = [checking] if checking is not None else None
        in_range = list(range(low, high + 1)) if low is not None and high is not None else None
        swapped_highlight = [checking] if found is True and checking is not None else None

        fig = create_bar_chart(
            arr,
            comparing=highlight_compare,
            swapped=swapped_highlight,
            sorted_indices=in_range,
            title=f"Search — Step {step_idx + 1}/{total}",
        )
        st.plotly_chart(fig, use_container_width=True)

        mc1, mc2, mc3 = st.columns(3)
        mc1.metric("Comparisons", current.get("comparisons", 0))
        mc2.metric("Checking Index", checking if checking is not None else "—")
        status = "Searching..." if found is None else ("Found!" if found else "Not Found")
        mc3.metric("Status", status)

        st.markdown("**Legend:** 🟢 Search range  |  🟡 Currently checking  |  🔴 Found")
    else:
        st.info("Configure and click **Search** to start.")

st.markdown("---")
st.markdown("### Algorithm Reference")
rows = []
for name, m in ALGORITHMS.items():
    rows.append({
        "Algorithm": name.replace("_", " ").title(),
        "Best": m["time_best"], "Average": m["time_avg"],
        "Worst": m["time_worst"], "Space": m["space"],
    })
st.dataframe(rows, use_container_width=True, hide_index=True)
