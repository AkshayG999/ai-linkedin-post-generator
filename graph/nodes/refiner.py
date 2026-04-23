from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

from graph.state import PostState
from prompts.refiner_prompt import REFINER_SYSTEM, REFINER_HUMAN

DIMENSIONS = [
    "hook_strength",
    "engagement_potential",
    "linkedin_algorithm_score",
    "eeat_score",
    "readability",
    "cta_quality",
]


def _build_scores_summary(scores: dict) -> str:
    lines = []
    for dim in DIMENSIONS:
        val = scores.get(dim, "N/A")
        lines.append(f"- {dim.replace('_', ' ').title()}: {val}/10")
    lines.append(f"- Total: {scores.get('total', 'N/A')}/60")
    return "\n".join(lines)


def _build_weak_dimensions(scores: dict) -> str:
    weak = [
        f"- {dim.replace('_', ' ').title()} ({scores.get(dim, 0)}/10)"
        for dim in DIMENSIONS
        if float(scores.get(dim, 0)) < 8
    ]
    return "\n".join(weak) if weak else "All dimensions scored 8 or above."


def refiner_node(state: PostState) -> PostState:
    """
    Node 7 – Refiner
    Rewrites the best draft to address critique, targeting weak scoring dimensions.
    """
    # Use the "refined" scores if available, else best-draft scores
    all_scores = state.get("evaluation_scores", {})
    scores = all_scores.get("refined", None)
    if scores is None:
        # Find the scores for the currently selected draft
        drafts = state.get("drafts", [])
        best_index = 0
        best_total = -1.0
        for i in range(len(drafts)):
            entry = all_scores.get(i, {})
            total = float(entry.get("total", 0))
            if total > best_total:
                best_total = total
                best_index = i
        scores = all_scores.get(best_index, {})

    llm = ChatOpenAI(model="gpt-4o", temperature=0.6)
    messages = [
        SystemMessage(content=REFINER_SYSTEM),
        HumanMessage(content=REFINER_HUMAN.format(
            current_draft=state.get("current_draft", ""),
            scores_summary=_build_scores_summary(scores),
            critique=state.get("critique", ""),
            weak_dimensions=_build_weak_dimensions(scores),
        )),
    ]
    response = llm.invoke(messages)
    refined = response.content.strip()

    return {
        **state,
        "current_draft": refined,
        "iteration_count": state.get("iteration_count", 0) + 1,
    }
