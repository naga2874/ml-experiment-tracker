# Mini Experiment Tracker

A tiny version of tools like MLflow / Weights & Biases. It's a "notebook"
for your machine learning experiments: it remembers what settings you
tried, what results you got, and lets you compare experiments in a
web dashboard.

## How it works (in plain English)

- `tracker/db.py` — the notebook itself (a SQLite database file). Knows
  how to save and read experiment data.
- `tracker/__init__.py` — a friendly assistant you actually talk to in
  your training code (`tracker.log_metric(...)` etc). It remembers which
  experiment is "currently running" so you don't have to.
- `example_train.py` — a toy example that trains a model 3 different ways
  and logs everything using the tracker.
- `dashboard.py` — a website (built with Streamlit) that reads the
  notebook and shows you tables and charts.

## How to run it

```bash
pip install -r requirements.txt

# Run some experiments (creates experiments.db automatically)
python example_train.py

# View the results in your browser
streamlit run dashboard.py
```

## How to use it in YOUR OWN training script

```python
import tracker

with tracker.start_run(name="my_experiment"):
    tracker.log_param("learning_rate", 0.001)

    for step in range(10):
        loss = train_one_step()  # your own training code
        tracker.log_metric("loss", loss, step=step)

    tracker.log_artifact("my_model.pt")
```

That's it — every run gets automatically saved and shows up in the dashboard.

## What's next (ideas to extend this)

- Add support for saving images/plots as artifacts, not just models
- Add a "delete run" button in the dashboard
- Add tags/filters so you can search runs by name
- Move from SQLite to Postgres if multiple people need to share one tracker
