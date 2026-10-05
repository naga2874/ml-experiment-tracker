# ML Experiment Tracker

A lightweight MLflow-style tool to log, compare and analyze machine learning
experiments, with an LLM assistant that suggests what to try next.

![Dashboard](screenshot.png)

## Features
- Log parameters, metrics and artifacts from any training script
- SQLite storage, no setup needed
- Streamlit dashboard to compare runs and plot any metric
- AI assistant (Gemini API) that analyzes runs and recommends next experiments

## How to run
1. Install: `pip install -r requirements.txt`
2. Create sample runs: `python example_train.py`
3. Set your free Gemini key (from aistudio.google.com): `set GEMINI_API_KEY=your_key`
4. Start the dashboard: `streamlit run dashboard.py`

## Use it in your own training code
import tracker

with tracker.start_run(name="my_experiment"):
    tracker.log_param("learning_rate", 0.01)
    tracker.log_metric("accuracy", 0.92, step=1)

## Tech stack
Python, SQLite, Pandas, Streamlit, Google Gemini API
