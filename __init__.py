"""
tracker/__init__.py
--------------------
This is the "friendly robot assistant" you actually talk to in your
training script. Instead of remembering run_id yourself and passing
it to every function, you say:

    import tracker

    with tracker.start_run("my_experiment"):
        tracker.log_param("learning_rate", 0.01)
        tracker.log_metric("loss", 0.9, step=1)
        tracker.log_metric("loss", 0.4, step=2)

The robot remembers "oh, we're currently on run abc123" and quietly
writes everything to the right page in the notebook for you.
"""

from . import db

# This is the robot's memory of "which page are we currently on".
_current_run_id = None


class RunContext:
    """
    This little class lets us use the "with tracker.start_run():" style.
    When you enter the 'with' block, it opens a new page.
    When you leave the 'with' block (even if your code crashes!),
    it automatically closes the page and marks it finished.
    """

    def __init__(self, run_id):
        self.run_id = run_id

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        global _current_run_id
        status = "failed" if exc_type is not None else "finished"
        db.finish_run(self.run_id, status=status)
        _current_run_id = None
        # returning False means: if there was an error, don't hide it,
        # let Python still show it to the user.
        return False


def start_run(name="unnamed_run"):
    """
    Call this at the start of your experiment. It creates a new
    notebook page and remembers it as the "current" one.
    """
    global _current_run_id
    db.init_db()  # make sure the notebook has its pages drawn/ready
    run_id = db.create_run(name)
    _current_run_id = run_id
    print(f"[tracker] Started run '{name}' with id={run_id}")
    return RunContext(run_id)


def log_param(key, value):
    """Writes a setting to whichever run is currently active."""
    if _current_run_id is None:
        raise RuntimeError("No active run! Call tracker.start_run() first.")
    db.log_param(_current_run_id, key, value)


def log_metric(key, value, step=0):
    """Writes a measurement to whichever run is currently active."""
    if _current_run_id is None:
        raise RuntimeError("No active run! Call tracker.start_run() first.")
    db.log_metric(_current_run_id, key, value, step)


def log_artifact(file_path, file_type="model"):
    """Remembers a saved model file for whichever run is currently active."""
    if _current_run_id is None:
        raise RuntimeError("No active run! Call tracker.start_run() first.")
    db.log_artifact(_current_run_id, file_path, file_type)
