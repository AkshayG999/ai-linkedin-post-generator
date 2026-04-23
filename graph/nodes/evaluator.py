import json
import re

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

from graph.state import PostState
from prompts.evaluator_prompt import EVALUATOR_SYSTEM, EVALUATOR_HUMAN

DIMENSIONS = [
    "hook_strength",
    "engagement_potential",
    "linkedin_algorithm_score",
    "eeat_score",
    "readability",
    "cta_quality",
]


def _parse_scores(raw: str) -> dict:
    """Extract JSON from LLM output, handling markdown code fences."""
    raw = raw.strip()
    # Strip ```json ... ``` fences if present
    fenced = re.search(r"```(?:json)?\s*([\s\S]+?)\s*```", raw)
    if fenced:
        raw = fenced.group(1)
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        # Fallback: assign neutral scores
        data = {d: 5 for d in DIMENSIONS}
        data["total"] = 30
        data["critique"] = "Could not parse evaluation scores."
    return data


def _evaluate_single(llm: ChatOpenAI, draft: str, state: PostState) -> dict:
    messages = [
        SystemMessage(content=EVALUATOR_SYSTEM),
        HumanMessage(content=EVALUATOR_HUMAN.format(
            keywords=state["keywords"],
            audience_profile=state["audience_profile"],
            draft=draft,
        )),
    ]
    response = llm.invoke(messages)
    return _parse_scores(response.content)


def evaluator_node(state: PostState) -> PostState:
    """
    Node 5 – Evaluator
    Scores each draft on a 6-dimension rubric and selects the best one.
    """
    llm = ChatOpenAI(model="gpt-4o", temperature=0.0)
    drafts = state.get("drafts", [])

    scores: dict = {}
    for i, draft in enumerate(drafts):
        scores[i] = _evaluate_single(llm, draft, state)

    return {
        **state,
        "evaluation_scores": scores,
    }


def re_evaluator_node(state: PostState) -> PostState:
    """
    Node 8 – Re-Evaluator
    Re-scores only the current (refined) draft using the same rubric.
    """
    llm = ChatOpenAI(model="gpt-4o", temperature=0.0)
    draft = state.get("current_draft", "")
    score = _evaluate_single(llm, draft, state)

    # Store re-evaluation under key "refined"
    existing = dict(state.get("evaluation_scores", {}))
    existing["refined"] = score

    return {
        **state,
        "evaluation_scores": existing,
    }
