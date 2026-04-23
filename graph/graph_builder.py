from langgraph.graph import StateGraph, START, END

from graph.state import PostState
from graph.nodes.research import research_node
from graph.nodes.audience import audience_profiler_node
from graph.nodes.outline import outline_node
from graph.nodes.drafting import multi_draft_node
from graph.nodes.evaluator import evaluator_node, re_evaluator_node
from graph.nodes.selector import selector_node
from graph.nodes.refiner import refiner_node
from graph.nodes.hashtags import hashtag_optimizer_node
from graph.nodes.formatter import formatter_node

QUALITY_THRESHOLD = 48.0   # out of 60 (average 8/10 across 6 dimensions)
MAX_ITERATIONS = 3


def _should_refine(state: PostState) -> str:
    """
    Conditional edge after re_evaluator_node.
    Returns "refiner" to loop or "hashtag_optimizer" to proceed to finalization.
    """
    scores = state.get("evaluation_scores", {})
    refined_scores = scores.get("refined", {})
    total = float(refined_scores.get("total", 0))
    iterations = state.get("iteration_count", 0)

    if total >= QUALITY_THRESHOLD or iterations >= MAX_ITERATIONS:
        return "hashtag_optimizer"
    return "refiner"


def build_graph() -> StateGraph:
    """
    Assembles and compiles the LangGraph StateGraph for LinkedIn post generation.

    Flow:
        START
          → research_node
          → audience_profiler_node
          → outline_node
          → multi_draft_node
          → evaluator_node
          → selector_node
          → refiner_node
          → re_evaluator_node
          → [conditional]
               if quality >= threshold OR iterations >= 3  → hashtag_optimizer_node
               else                                        → refiner_node (loop)
          → hashtag_optimizer_node
          → formatter_node
          → END
    """
    graph = StateGraph(PostState)

    # Register nodes
    graph.add_node("research", research_node)
    graph.add_node("audience_profiler", audience_profiler_node)
    graph.add_node("outline", outline_node)
    graph.add_node("multi_draft", multi_draft_node)
    graph.add_node("evaluator", evaluator_node)
    graph.add_node("selector", selector_node)
    graph.add_node("refiner", refiner_node)
    graph.add_node("re_evaluator", re_evaluator_node)
    graph.add_node("hashtag_optimizer", hashtag_optimizer_node)
    graph.add_node("formatter", formatter_node)

    # Linear edges
    graph.add_edge(START, "research")
    graph.add_edge("research", "audience_profiler")
    graph.add_edge("audience_profiler", "outline")
    graph.add_edge("outline", "multi_draft")
    graph.add_edge("multi_draft", "evaluator")
    graph.add_edge("evaluator", "selector")
    graph.add_edge("selector", "refiner")
    graph.add_edge("refiner", "re_evaluator")

    # Conditional refinement loop
    graph.add_conditional_edges(
        "re_evaluator",
        _should_refine,
        {
            "refiner": "refiner",
            "hashtag_optimizer": "hashtag_optimizer",
        },
    )

    graph.add_edge("hashtag_optimizer", "formatter")
    graph.add_edge("formatter", END)

    return graph.compile()
