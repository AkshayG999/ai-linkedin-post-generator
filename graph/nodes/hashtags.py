import json
import re

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

from graph.state import PostState
from prompts.hashtag_prompt import HASHTAG_SYSTEM, HASHTAG_HUMAN

_HASHTAG_RE = re.compile(r"#\w+")


def _parse_hashtag_response(raw: str) -> list[str]:
    raw = raw.strip()
    fenced = re.search(r"```(?:json)?\s*([\s\S]+?)\s*```", raw)
    if fenced:
        raw = fenced.group(1)
    try:
        data = json.loads(raw)
        return data.get("hashtags", [])
    except json.JSONDecodeError:
        # Fallback: extract any #Tags directly from the response
        return _HASHTAG_RE.findall(raw)[:5]


def _replace_hashtags(post: str, new_tags: list[str]) -> str:
    """Remove all existing hashtags from the post body and append the new set."""
    # Strip existing hashtags
    cleaned = re.sub(r"\s*#\w+", "", post).rstrip()
    tag_line = " ".join(new_tags)
    return f"{cleaned}\n\n{tag_line}"


def hashtag_optimizer_node(state: PostState) -> PostState:
    """
    Node 9 – Hashtag Optimizer
    Replaces hashtags in the current draft with optimally selected ones.
    """
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)
    messages = [
        SystemMessage(content=HASHTAG_SYSTEM),
        HumanMessage(content=HASHTAG_HUMAN.format(
            keywords=state["keywords"],
            post_type=state["post_type"],
        )),
    ]
    response = llm.invoke(messages)
    new_tags = _parse_hashtag_response(response.content)

    post = state.get("current_draft", "")
    optimized = _replace_hashtags(post, new_tags)

    return {
        **state,
        "final_post": optimized,
    }
