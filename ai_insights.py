from google import genai
from tracker import db

MODEL = "gemini-3.5-flash"


def build_summary(run_ids, names):
    """Turns selected runs into plain text the AI can read."""
    lines = []
    for run_id in run_ids:
        params = dict(db.get_params(run_id))
        final_metrics = {}
        for key, value, step in db.get_metrics(run_id):
            final_metrics[key] = value  # last value wins
        lines.append(
            f"Run '{names[run_id]}' ({run_id}): "
            f"params={params}, final_metrics={final_metrics}"
        )
    return "\n".join(lines)


def ask_ai(summary, question):
    """Sends the experiment data and your question to the AI."""
    client = genai.Client()  # reads GEMINI_API_KEY from your terminal
    prompt = (
        "You are an ML experiment analyst. Use only the data given. "
        "Be concise. Compare the runs, point out which settings helped, "
        "and suggest 2-3 specific next experiments.\n\n"
        f"Experiments:\n{summary}\n\nQuestion: {question}"
    )
    response = client.models.generate_content(model=MODEL, contents=prompt)
    return response.text