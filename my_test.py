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

# Table of all runs
runs_df = pd.DataFrame(runs, columns=["run_id", "name", "created_at", "status"])
runs_df["created_at"] = pd.to_datetime(runs_df["created_at"], unit="s")

st.subheader("All experiments")
st.dataframe(runs_df, use_container_width=True)

# Compare runs
st.subheader("Compare experiments")

names = dict(zip(runs_df["run_id"], runs_df["name"]))

selected_ids = st.multiselect(
    "Pick one or more runs to compare",
    options=runs_df["run_id"].tolist(),
    default=[runs_df["run_id"].iloc[0]],
    format_func=lambda r: f"{names[r]} ({r})",
)

if selected_ids:
    st.write("**Settings used:**")
    param_rows = []
    for run_id in selected_ids:
        params = dict(db.get_params(run_id))
        params["run_id"] = run_id
        param_rows.append(params)
    st.dataframe(pd.DataFrame(param_rows), use_container_width=True)

    # Collect metrics: {metric_name: {run_id: {step: value}}}
    all_metrics = {}
    for run_id in selected_ids:
        for key, value, step in db.get_metrics(run_id):
            all_metrics.setdefault(key, {}).setdefault(run_id, {})[step] = value

    if all_metrics:
        chosen = st.selectbox("Pick a metric to plot", sorted(all_metrics))
        st.write(f"**{chosen} over time (per run):**")
        st.line_chart(pd.DataFrame(all_metrics[chosen]))
    else:
        st.write("No metrics logged for the selected run(s).")