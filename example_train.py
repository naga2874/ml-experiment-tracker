"""
example_train.py
-----------------
This is a PRETEND science experiment. We're training a simple model
on the classic "Iris flowers" dataset (predicting flower type from
measurements). We run it a few times with different settings, and
our tracker writes everything down in the notebook automatically.

Run this with:  python example_train.py
"""

import pickle
import os
import sys

# Let Python find our "tracker" folder
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import tracker
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Load the flower data once
X, y = load_iris(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# We'll try a few different "settings" (like trying more sunlight/less sunlight)
settings_to_try = [
    {"n_estimators": 10, "max_depth": 2},
    {"n_estimators": 50, "max_depth": 4},
    {"n_estimators": 100, "max_depth": None},
    {"n_estimators": 200, "max_depth": 6},
]

os.makedirs("artifacts", exist_ok=True)

for settings in settings_to_try:
    # Start a new "page" in the notebook for this experiment
    with tracker.start_run(name="iris_random_forest") as run:

        # Write down what settings we're using
        tracker.log_param("n_estimators", settings["n_estimators"])
        tracker.log_param("max_depth", settings["max_depth"])

        # Train the model
        model = RandomForestClassifier(**settings, random_state=42)

        # Pretend we check progress every few trees (simulated steps)
        for step in range(1, 4):
            model.n_estimators = max(1, settings["n_estimators"] * step // 3)
            model.fit(X_train, y_train)
            preds = model.predict(X_test)
            acc = accuracy_score(y_test, preds)
            tracker.log_metric("accuracy", acc, step=step)
            print(f"  step {step}: accuracy = {acc:.3f}")

        # Save the final trained model to disk, and tell the tracker where it is
        model_path = f"artifacts/model_{run.run_id}.pkl"
        with open(model_path, "wb") as f:
            pickle.dump(model, f)
        tracker.log_artifact(model_path, file_type="sklearn_model")

print("\nAll experiments done! Run `streamlit run dashboard.py` to see the results.")
