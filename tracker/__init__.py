"""
tracker/__init__.py
--------------------
The friendly robot assistant you talk to in your training script.
Instead of remembering run_id yourself and passing it to every
function, you say:

    import tracker

    with tracker.start_run("my_experiment"):
        tracker.log_param("learning_rate", 0.01)
        tracker.log_metric("loss", 0.9, step=1)

The robot remembers "which page we're currently on" and quietly
writes everything to the right place in the notebook for you.
"""

from . import db

_current_run_id = None


class RunContext:
    def __init__(self, run_id):
        self.run_id = run_id

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        global _current_run_id
        status = "failed" if exc_type is not None else "finished"
        db.finish_run(self.run_id, status=status)
        _current_run_id = None
        return False


def start_run(name="unnamed_run"):
    global _current_run_id
    db.init_db()
    run_id = db.create_run(name)
    _current_run_id = run_id
    print(f"[tracker] Started run '{name}' with id={run_id}")
    return RunContext(run_id)


def log_param(key, value):
    if _current_run_id is None:
        raise RuntimeError("No active run! Call tracker.start_run() first.")
    db.log_param(_current_run_id, key, value)


def log_metric(key, value, step=0):
    if _current_run_id is None:
        raise RuntimeError("No active run! Call tracker.start_run() first.")
    db.log_metric(_current_run_id, key, value, step)


def log_artifact(file_path, file_type="model"):
    if _current_run_id is None:
        raise RuntimeError("No active run! Call tracker.start_run() first.")
    db.log_artifact(_current_run_id, file_path, file_type)