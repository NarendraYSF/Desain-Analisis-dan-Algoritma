import streamlit as st

from algorithms.sorting import ALGORITHMS
from core.tracer import collect_steps, get_step
from core.visualizer import create_bar_chart
from utils.data_generator import random_array, sorted_array, reversed_array, nearly_sorted_array

st.set_page_config(page_title="Sorting Visualizer", layout="wide")
st.title("Sorting Visualizer")
st.markdown("Step-by-step visualization of 8 sorting algorithms")

col_cfg, col_viz = st.columns([1, 3])

with col_cfg:
    algo_name = st.selectbox("Algorithm", list(ALGORITHMS.keys()), format_func=str.title)
    meta = ALGORITHMS[algo_name]
    st.markdown(f"**Time:** `{meta['time']}`  |  **Space:** `{meta['space']}`  |  **Stable:** `{meta['stable']}`")

    dist = st.selectbox("Data Distribution", ["Random", "Sorted", "Reversed", "Nearly Sorted"])
    size = st.slider("Array Size", 5, 60, 20)

    gen_map = {
        "Random": lambda: random_array(size, 1, 100),
        "Sorted": lambda: sorted_array(size),
        "Reversed": lambda: reversed_array(size),
        "Nearly Sorted": lambda: nearly_sorted_array(size),
    }

    if st.button("Generate & Run", type="primary"):
        arr = gen_map[dist]()
        steps = collect_steps(meta["traced"](arr))
        st.session_state["sort_steps"] = steps
        st.session_state["sort_step_idx"] = 0
        st.session_state["sort_arr"] = arr

with col_viz:
    if "sort_steps" in st.session_state:
        steps = st.session_state["sort_steps"]
        total = len(steps)

        step_idx = st.slider("Step", 0, max(total - 1, 0), st.session_state.get("sort_step_idx", 0), key="sort_slider")
        st.session_state["sort_step_idx"] = step_idx

        current = get_step(steps, step_idx)
        arr = current.get("array", [])
        comparing = current.get("comparing")
        swapped = current.get("swapped")
        sorted_idx = current.get("sorted_indices", [])

        cmp_list = list(comparing) if comparing else None
        swp_list = list(swapped) if swapped else None

        fig = create_bar_chart(
            arr,
            comparing=cmp_list,
            swapped=swp_list,
            sorted_indices=sorted_idx,
            title=f"{algo_name.title()} Sort — Step {step_idx + 1}/{total}",
        )
        st.plotly_chart(fig, use_container_width=True)

        mc1, mc2, mc3 = st.columns(3)
        mc1.metric("Comparisons", current.get("comparisons", 0))
        mc2.metric("Swaps", current.get("swaps", 0))
        mc3.metric("Step", f"{step_idx + 1} / {total}")

        st.markdown("**Legend:** 🔵 Default  |  🟡 Comparing  |  🔴 Swapped  |  🟢 Sorted")
    else:
        st.info("Configure and click **Generate & Run** to start the visualization.")

st.markdown("---")
st.markdown("### Algorithm Comparison Table")
rows = []
for name, m in ALGORITHMS.items():
    rows.append({"Algorithm": name.title(), "Time": m["time"], "Space": m["space"], "Stable": "Yes" if m["stable"] else "No"})
st.dataframe(rows, use_container_width=True, hide_index=True)
