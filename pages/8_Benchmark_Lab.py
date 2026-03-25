import streamlit as st
import pandas as pd

from algorithms.sorting import ALGORITHMS as SORT_ALGOS
from algorithms.searching import ALGORITHMS as SEARCH_ALGOS
from core.benchmark import compare_algorithms
from core.visualizer import create_benchmark_chart
from utils.data_generator import random_array

st.set_page_config(page_title="Benchmark Lab", layout="wide")
st.title("Benchmark Lab")
st.markdown("Compare algorithms head-to-head with real performance measurements")

category = st.selectbox("Category", ["Sorting", "Searching"])

if category == "Sorting":
    all_algos = SORT_ALGOS
    default_selected = ["bubble", "merge", "quick", "heap"]
else:
    all_algos = SEARCH_ALGOS
    default_selected = list(all_algos.keys())

selected = st.multiselect(
    "Select Algorithms (2-5)",
    list(all_algos.keys()),
    default=default_selected,
    format_func=lambda x: x.replace("_", " ").title(),
)

col1, col2, col3 = st.columns(3)
with col1:
    sizes_str = st.text_input("Input Sizes (comma-separated)", "100, 500, 1000, 2000, 5000")
with col2:
    runs = st.number_input("Runs per size", 1, 10, 3)
with col3:
    max_val = st.number_input("Max array value", 10, 100000, 10000)

if st.button("Run Benchmark", type="primary"):
    if len(selected) < 2:
        st.error("Select at least 2 algorithms.")
    else:
        sizes = [int(x.strip()) for x in sizes_str.split(",")]
        algos = {name: all_algos[name]["plain"] for name in selected}

        if category == "Sorting":
            data_gen = lambda s: random_array(s, 1, max_val)
        else:
            def data_gen(s):
                arr = sorted(random_array(s, 1, max_val))
                return (arr, arr[s // 2])

            plain_wrappers = {}
            for name in selected:
                fn = all_algos[name]["plain"]
                plain_wrappers[name] = lambda data, f=fn: f(data[0], data[1])
            algos = plain_wrappers

        with st.spinner("Running benchmarks..."):
            df = compare_algorithms(algos, data_gen, sizes, runs=runs)

        st.session_state["bench_df"] = df

if "bench_df" in st.session_state:
    df = st.session_state["bench_df"]

    fig = create_benchmark_chart(df, title="Execution Time vs Input Size")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Results Table")
    display_df = df.copy()
    display_df["time_mean"] = display_df["time_mean"].apply(lambda x: f"{x:.6f}s")
    display_df["time_std"] = display_df["time_std"].apply(lambda x: f"{x:.6f}s")
    display_df["memory_peak"] = display_df["memory_peak"].apply(lambda x: f"{x / 1024:.1f} KB")
    st.dataframe(display_df, use_container_width=True, hide_index=True)

    csv = df.to_csv(index=False)
    st.download_button("Download CSV", csv, "benchmark_results.csv", "text/csv")
