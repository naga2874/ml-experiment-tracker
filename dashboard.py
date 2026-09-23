"""
dashboard.py
------------
This turns our boring notebook (database) into a pretty picture-book
website. Run it with:

    streamlit run dashboard.py

Streamlit is magic: we just write normal Python, and it turns into
a live website automatically. No HTML/CSS/JavaScript needed.
"""

import streamlit as st
import pandas as pd
from tracker import db

st.set_page_config(page_title="My Experiment Tracker", layout="wide")
st.title("🧪 My Experiment Tracker")
st.caption("Every experiment you've ever run, all in one place.")

db.init_db()
runs = db.get_all_runs()

if not runs:
    st.info("No experiments yet! Run `python example_train.py` first.")
    st.stop()

# --- Build a table of all runs, like a table of contents ---
runs_df = pd.DataFrame(runs, columns=["run_id", "name", "created_at", "status"])
runs_df["created_at"] = pd.to_datetime(runs_df["created_at"], unit="s")

st.subheader("All experiments")
st.dataframe(runs_df, use_container_width=True)

# --- Let the user pick runs to look at closely / compare ---
st.subheader("Compare experiments")
selected_ids = st.multiselect(
    "Pick one or more runs to compare",
    options=runs_df["run_id"].tolist(),
    default=[runs_df["run_id"].iloc[0]],
)

if selected_ids:
    # Show each selected run's settings side by side
    st.write("**Settings used:**")
    param_rows = []
    for run_id in selected_ids:
        params = dict(db.get_params(run_id))
        params["run_id"] = run_id
        param_rows.append(params)
    st.dataframe(pd.DataFrame(param_rows), use_container_width=True)

    # Show each selected run's metrics as a line chart, all on one graph
    st.write("**Accuracy over time (per run):**")
    chart_data = {}
    for run_id in selected_ids:
        metrics = db.get_metrics(run_id)
        for key, value, step in metrics:
            col_name = f"{run_id} - {key}"
            chart_data.setdefault(col_name, {})[step] = value

    if chart_data:
        chart_df = pd.DataFrame(chart_data)
        st.line_chart(chart_df)
    else:
        st.write("No metrics logged for the selected run(s).")
