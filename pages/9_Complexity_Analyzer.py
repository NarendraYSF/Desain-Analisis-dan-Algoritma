import streamlit as st

from algorithms.sorting import ALGORITHMS as SORT_ALGOS
from core.benchmark import benchmark_algorithm
from core.complexity import fit_complexity
from core.visualizer import create_complexity_chart
from utils.data_generator import random_array

st.set_page_config(page_title="Complexity Analyzer", layout="wide")
st.title("Complexity Analyzer")
st.markdown("Empirically determine algorithm time complexity via curve fitting")

col_cfg, col_res = st.columns([1, 2])

with col_cfg:
    algo_name = st.selectbox("Algorithm", list(SORT_ALGOS.keys()), format_func=str.title)
    meta = SORT_ALGOS[algo_name]
    st.markdown(f"**Theoretical Time:** `{meta['time']}`")

    sizes_str = st.text_input("Input Sizes", "50, 100, 200, 500, 1000, 2000, 3000, 5000")
    runs = st.number_input("Runs per size", 1, 10, 3)

    if st.button("Analyze Complexity", type="primary"):
        sizes = [int(x.strip()) for x in sizes_str.split(",")]
        with st.spinner("Benchmarking..."):
            df = benchmark_algorithm(
                meta["plain"],
                lambda s: random_array(s, 1, 10000),
                sizes,
                runs=runs,
            )

        times = df["time_mean"].tolist()
        result = fit_complexity(sizes, times)

        st.session_state["cx_sizes"] = sizes
        st.session_state["cx_times"] = times
        st.session_state["cx_result"] = result
        st.session_state["cx_df"] = df

with col_res:
    if "cx_result" in st.session_state:
        result = st.session_state["cx_result"]
        sizes = st.session_state["cx_sizes"]
        times = st.session_state["cx_times"]

        st.markdown(f"### Best Fit: `{result['best_fit']}`")
        st.markdown(f"**R² Score:** `{result['r_squared']:.4f}`")

        fig = create_complexity_chart(
            sizes, times,
            result["fitted_curves"],
            result["best_fit"],
            title=f"Complexity Analysis — {algo_name.title()} Sort",
        )
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("### All Fits (R² Scores)")
        fits_sorted = sorted(result["all_fits"].items(), key=lambda x: -x[1])
        rows = [{"Complexity": name, "R² Score": f"{r2:.4f}"} for name, r2 in fits_sorted]
        st.dataframe(rows, use_container_width=True, hide_index=True)

        st.markdown("### Benchmark Data")
        df = st.session_state["cx_df"]
        display = df.copy()
        display["time_mean"] = display["time_mean"].apply(lambda x: f"{x:.6f}s")
        display["time_std"] = display["time_std"].apply(lambda x: f"{x:.6f}s")
        display["memory_peak"] = display["memory_peak"].apply(lambda x: f"{x / 1024:.1f} KB")
        st.dataframe(display, use_container_width=True, hide_index=True)
    else:
        st.info("Select an algorithm and click **Analyze Complexity** to start.")

st.markdown("---")
st.markdown("### How It Works")
st.markdown("""
1. The algorithm runs on arrays of increasing sizes
2. Execution time is measured for each size (averaged over multiple runs)
3. The empirical data is fitted against candidate complexity functions using **SciPy curve_fit**
4. The function with the highest **R² score** (closest to 1.0) is selected as the best fit
5. Candidate functions: O(1), O(log n), O(n), O(n log n), O(n²), O(n³), O(2^n)
""")
