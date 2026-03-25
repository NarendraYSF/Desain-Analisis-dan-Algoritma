import streamlit as st

from algorithms.backtracking import ALGORITHMS
from core.tracer import collect_steps, get_step
from core.visualizer import create_board

st.set_page_config(page_title="Backtracking", layout="wide")
st.title("Backtracking Algorithms")
st.markdown("Watch backtracking explore and prune the search space")

col_cfg, col_viz = st.columns([1, 3])

with col_cfg:
    algo_name = st.selectbox("Problem", list(ALGORITHMS.keys()), format_func=lambda x: x.replace("_", " ").title())
    meta = ALGORITHMS[algo_name]
    st.markdown(f"**Time:** `{meta['time']}`  |  **Space:** `{meta['space']}`")

    if algo_name == "n_queens":
        n = st.slider("Board Size (N)", 4, 12, 8)
        params = lambda: {"n": n}
    elif algo_name == "sudoku":
        st.markdown("Enter Sudoku (9 rows, 0=empty):")
        default_board = [
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9],
        ]
        board_str = st.text_area("Board (comma rows, semicolon between rows)",
            "; ".join([", ".join(str(c) for c in row) for row in default_board]))
        def parse_board():
            rows = board_str.strip().split(";")
            return [[int(c.strip()) for c in row.split(",")] for row in rows]
        params = lambda: {"board": parse_board()}
    elif algo_name == "subset_sum":
        nums_str = st.text_input("Numbers", "3, 34, 4, 12, 5, 2")
        target = st.number_input("Target Sum", 1, 1000, 9)
        params = lambda: {
            "nums": [int(x.strip()) for x in nums_str.split(",")],
            "target": target,
        }
    else:
        params = lambda: {}

    if st.button("Run Backtracking", type="primary"):
        try:
            p = params()
            steps = collect_steps(meta["traced"](**p))
            st.session_state["bt_steps"] = steps
        except Exception as e:
            st.error(f"Error: {e}")

with col_viz:
    if "bt_steps" in st.session_state:
        steps = st.session_state["bt_steps"]
        total = len(steps)
        step_idx = st.slider("Step", 0, max(total - 1, 0), 0, key="bt_slider")
        current = get_step(steps, step_idx)

        if algo_name == "n_queens":
            board = current.get("board", [])
            placing = current.get("placing")
            conflict = current.get("conflict", False)
            queens = current.get("queens_placed", 0)
            backtracks = current.get("backtracks", 0)

            highlights = set()
            if placing:
                highlights.add(placing)
            queen_map = []
            for i, row in enumerate(board):
                queen_row = []
                for j, val in enumerate(row):
                    queen_row.append("Q" if val == 1 else "")
                queen_map.append(queen_row)

            fig = create_board(queen_map, highlights=highlights, title=f"N-Queens — Step {step_idx + 1}/{total}")
            st.plotly_chart(fig, use_container_width=True)

            mc1, mc2, mc3 = st.columns(3)
            mc1.metric("Queens Placed", queens)
            mc2.metric("Backtracks", backtracks)
            mc3.metric("Conflict", "Yes" if conflict else "No")

        elif algo_name == "sudoku":
            board = current.get("board", [])
            trying = current.get("trying")
            valid = current.get("valid", True)
            backtracks = current.get("backtracks", 0)

            highlights = set()
            if trying:
                highlights.add((trying[0], trying[1]))

            fig = create_board(board, highlights=highlights, title=f"Sudoku — Step {step_idx + 1}/{total}")
            st.plotly_chart(fig, use_container_width=True)

            mc1, mc2, mc3 = st.columns(3)
            mc1.metric("Step", f"{step_idx + 1}/{total}")
            mc2.metric("Backtracks", backtracks)
            if trying:
                mc3.metric("Trying", f"({trying[0]},{trying[1]})={trying[2]}")

        elif algo_name == "subset_sum":
            subset = current.get("current_subset", [])
            remaining = current.get("remaining", 0)
            decision = current.get("decision", "")
            backtracks = current.get("backtracks", 0)

            st.markdown(f"### Step {step_idx + 1} / {total}")
            mc1, mc2, mc3 = st.columns(3)
            mc1.metric("Current Subset", str(subset))
            mc2.metric("Remaining", remaining)
            mc3.metric("Backtracks", backtracks)
            if decision:
                st.info(f"**Decision:** {decision}")
    else:
        st.info("Configure and click **Run Backtracking** to start.")
