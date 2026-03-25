import streamlit as st

st.set_page_config(
    page_title="AlgoLab - Algorithm Design & Analysis",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .algo-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem; border-radius: 12px; color: white;
        margin-bottom: 1rem; box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .algo-card h3 { margin: 0 0 0.5rem 0; }
    .algo-card p { margin: 0; opacity: 0.9; font-size: 0.95rem; }
    .metric-card {
        background: #f8f9fa; padding: 1.2rem; border-radius: 10px;
        border-left: 4px solid #667eea; margin-bottom: 0.8rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("AlgoLab")
st.markdown("### Algorithm Design & Analysis Platform")
st.markdown("---")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Algorithms", "30+", help="Total implemented algorithms")
with col2:
    st.metric("Categories", "7", help="Algorithm categories")
with col3:
    st.metric("Tools", "2", help="Benchmark Lab & Complexity Analyzer")

st.markdown("---")
st.markdown("## Algorithm Categories")

categories = [
    {
        "name": "Sorting Algorithms",
        "page": "1_Sorting_Visualizer",
        "desc": "Bubble, Selection, Insertion, Merge, Quick, Heap, Counting, Radix",
        "count": 8,
    },
    {
        "name": "Searching Algorithms",
        "page": "2_Searching_Algorithms",
        "desc": "Linear Search, Binary Search, Interpolation Search",
        "count": 3,
    },
    {
        "name": "Graph Algorithms",
        "page": "3_Graph_Algorithms",
        "desc": "BFS, DFS, Dijkstra, Bellman-Ford, Prim, Kruskal, Topological Sort",
        "count": 7,
    },
    {
        "name": "Dynamic Programming",
        "page": "4_Dynamic_Programming",
        "desc": "Knapsack, LCS, Edit Distance, Coin Change, MCM, LIS",
        "count": 6,
    },
    {
        "name": "Greedy Algorithms",
        "page": "5_Greedy_Algorithms",
        "desc": "Activity Selection, Fractional Knapsack, Huffman Coding",
        "count": 3,
    },
    {
        "name": "Backtracking",
        "page": "6_Backtracking",
        "desc": "N-Queens, Sudoku Solver, Subset Sum",
        "count": 3,
    },
    {
        "name": "Divide & Conquer",
        "page": "7_Divide_and_Conquer",
        "desc": "Merge Sort Tree, Closest Pair of Points, Karatsuba Multiplication",
        "count": 3,
    },
]

cols = st.columns(3)
for i, cat in enumerate(categories):
    with cols[i % 3]:
        st.markdown(
            f"""<div class="algo-card">
            <h3>{cat['name']}</h3>
            <p>{cat['desc']}</p>
            <p style="margin-top:0.5rem;font-weight:bold;">{cat['count']} algorithms</p>
            </div>""",
            unsafe_allow_html=True,
        )

st.markdown("---")
st.markdown("## Analysis Tools")

t1, t2 = st.columns(2)
with t1:
    st.markdown(
        """<div class="metric-card">
        <h4>Benchmark Lab</h4>
        <p>Compare algorithms head-to-head. Measure execution time and memory usage
        across different input sizes. Export results to CSV.</p>
        </div>""",
        unsafe_allow_html=True,
    )
with t2:
    st.markdown(
        """<div class="metric-card">
        <h4>Complexity Analyzer</h4>
        <p>Empirically measure algorithm complexity. Curve fitting to O(1), O(log n),
        O(n), O(n log n), O(n²), O(n³), O(2^n) with R² confidence scores.</p>
        </div>""",
        unsafe_allow_html=True,
    )

st.markdown("---")
st.markdown("## Big-O Complexity Reference")

ref_data = {
    "Complexity": [
        "O(1)", "O(log n)", "O(n)", "O(n log n)",
        "O(n²)", "O(n³)", "O(2^n)", "O(n!)",
    ],
    "Name": [
        "Constant", "Logarithmic", "Linear", "Linearithmic",
        "Quadratic", "Cubic", "Exponential", "Factorial",
    ],
    "n=10": [
        "1", "3.3", "10", "33", "100", "1,000", "1,024", "3,628,800",
    ],
    "n=100": [
        "1", "6.6", "100", "664", "10,000", "1,000,000", "1.27×10³⁰", "9.33×10¹⁵⁷",
    ],
    "n=1000": [
        "1", "10", "1,000", "9,966", "1,000,000", "10⁹", "∞", "∞",
    ],
    "Example Algorithms": [
        "Hash lookup",
        "Binary Search",
        "Linear Search",
        "Merge Sort, Quick Sort (avg)",
        "Bubble Sort, Selection Sort",
        "Matrix Multiplication (naive)",
        "Subset Sum (brute force)",
        "Traveling Salesman (brute force)",
    ],
}
st.dataframe(ref_data, use_container_width=True, hide_index=True)

st.markdown("---")
st.markdown(
    "<p style='text-align:center;color:#888;'>AlgoLab — Built for Algorithm Design & Analysis</p>",
    unsafe_allow_html=True,
)
