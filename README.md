# AlgoLab — Algorithm Design & Analysis Platform

Interactive web application for visualizing, benchmarking, and analyzing algorithms.
Built with Python and Streamlit.

## Features

### Algorithm Visualizers (7 categories, 30+ algorithms)

| Category | Algorithms | Visualization |
|----------|-----------|---------------|
| **Sorting** | Bubble, Selection, Insertion, Merge, Quick, Heap, Counting, Radix | Animated bar charts with step-by-step comparisons/swaps |
| **Searching** | Linear, Binary, Interpolation | Highlighted search range and target tracking |
| **Graph** | BFS, DFS, Dijkstra, Bellman-Ford, Prim, Kruskal, Topological Sort | Interactive network graphs with colored traversal |
| **Dynamic Programming** | 0/1 Knapsack, LCS, Edit Distance, Coin Change, MCM, LIS | Heatmap table filling animation |
| **Greedy** | Activity Selection, Fractional Knapsack, Huffman Coding | Timeline charts and tree visualizations |
| **Backtracking** | N-Queens, Sudoku Solver, Subset Sum | Board visualizations with backtrack counters |
| **Divide & Conquer** | Merge Sort Tree, Closest Pair, Karatsuba | Recursion depth tracking and scatter plots |

### Analysis Tools

- **Benchmark Lab** — Compare 2-5 algorithms head-to-head with real timing and memory measurements. Export results to CSV.
- **Complexity Analyzer** — Empirically determine time complexity via curve fitting (O(1) through O(2^n)) with R² confidence scores.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

The app opens at `http://localhost:8501`. Use the sidebar to navigate between pages.

## Project Structure

```
Algo/
├── app.py                          # Home dashboard
├── requirements.txt                # Python dependencies
├── pages/
│   ├── 1_Sorting_Visualizer.py     # Sorting step-by-step animation
│   ├── 2_Searching_Algorithms.py   # Search visualization
│   ├── 3_Graph_Algorithms.py       # Graph traversal & MST
│   ├── 4_Dynamic_Programming.py    # DP table visualization
│   ├── 5_Greedy_Algorithms.py      # Greedy choice display
│   ├── 6_Backtracking.py           # Board & tree visualization
│   ├── 7_Divide_and_Conquer.py     # Recursion visualization
│   ├── 8_Benchmark_Lab.py          # Performance comparison
│   └── 9_Complexity_Analyzer.py    # Empirical Big-O detection
├── algorithms/                     # Pure algorithm implementations
│   ├── sorting.py                  # 8 sorting algorithms
│   ├── searching.py                # 3 search algorithms
│   ├── graph.py                    # 7 graph algorithms
│   ├── dynamic_programming.py      # 6 DP problems
│   ├── greedy.py                   # 3 greedy algorithms
│   ├── backtracking.py             # 3 backtracking problems
│   └── divide_conquer.py           # 3 D&C algorithms
├── core/                           # Engine modules
│   ├── tracer.py                   # Step collection from generators
│   ├── benchmark.py                # Timing & memory measurement
│   ├── complexity.py               # Curve fitting to Big-O
│   └── visualizer.py               # Plotly chart builders
└── utils/                          # Helpers
    ├── data_generator.py           # Array, graph, point generators
    └── graph_utils.py              # Graph format conversions
```

## Tech Stack

- **Streamlit** — Multi-page web framework
- **Plotly** — Interactive charts and visualizations
- **NetworkX** — Graph layout computation
- **NumPy** — Numerical operations
- **SciPy** — Curve fitting for complexity analysis
- **Pandas** — Benchmark data handling

## Architecture

Each algorithm is implemented as a **Python generator** that yields state dictionaries at every step. This enables:

1. **Step-by-step visualization** — Slider controls which step to display
2. **Decoupled logic** — Algorithms know nothing about visualization
3. **Benchmarkable** — Plain (non-generator) versions run without overhead

The `core/` modules bridge algorithms and UI:
- `tracer.py` collects generator steps into lists
- `benchmark.py` measures time and memory across input sizes
- `complexity.py` fits empirical data to Big-O functions
- `visualizer.py` creates Plotly figures from algorithm state
