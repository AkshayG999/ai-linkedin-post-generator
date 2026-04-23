from graph.state import PostState
from graph.nodes.utils import get_best_draft_index


def selector_node(state: PostState) -> PostState:
    """
    Node 6 – Selector (no LLM needed)
    Picks the highest-scoring draft and extracts the critique for the refiner.
    """
    drafts = state.get("drafts", [])
    scores = state.get("evaluation_scores", {})

    best_index = get_best_draft_index(drafts, scores)
    best_draft = drafts[best_index] if drafts else ""
    critique = scores.get(best_index, {}).get("critique", "No critique available.")

    return {
        **state,
        "current_draft": best_draft,
        "critique": critique,
        "iteration_count": state.get("iteration_count", 0),
    }
