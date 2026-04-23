from graph.state import PostState


def selector_node(state: PostState) -> PostState:
    """
    Node 6 – Selector (no LLM needed)
    Picks the highest-scoring draft and extracts the critique for the refiner.
    """
    drafts = state.get("drafts", [])
    scores = state.get("evaluation_scores", {})

    best_index = 0
    best_total = -1.0

    for i in range(len(drafts)):
        entry = scores.get(i, {})
        total = float(entry.get("total", 0))
        if total > best_total:
            best_total = total
            best_index = i

    best_draft = drafts[best_index] if drafts else ""
    critique = scores.get(best_index, {}).get("critique", "No critique available.")

    return {
        **state,
        "current_draft": best_draft,
        "critique": critique,
        "iteration_count": state.get("iteration_count", 0),
    }
