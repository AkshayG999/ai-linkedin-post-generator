import re

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

from graph.state import PostState

FORMATTER_SYSTEM = (
    "You are a LinkedIn post formatter. Your ONLY job is to apply final formatting "
    "rules to the provided post text. Do NOT change the content, wording, or structure. "
    "Return only the formatted post text."
)

FORMATTER_HUMAN = """
Apply these LinkedIn formatting rules to the post below:

1. Each sentence or short thought should be on its own line (mobile-friendly).
2. Emojis should appear at the start of the hook line and at major section transitions only (not every line).
3. Replace all em-dashes (—) with a comma or colon as appropriate.
4. Ensure there are exactly 3–5 hashtags at the very end, on their own line.
5. If there are URLs in the body, replace them with "(link in comments)".
6. Wrap key phrases in *asterisks* for emphasis (maximum 3 emphases per post).
7. Ensure the post ends with the hashtags and nothing after them.

Post Type: {post_type}
Target Length: {length}

**Post to Format:**
{post}

Return ONLY the formatted post. No commentary, no preamble.
"""


def formatter_node(state: PostState) -> PostState:
    """
    Node 10 – Formatter
    Applies final LinkedIn-specific formatting to the post before display.
    """
    post = state.get("final_post", state.get("current_draft", ""))
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.0)
    messages = [
        SystemMessage(content=FORMATTER_SYSTEM),
        HumanMessage(content=FORMATTER_HUMAN.format(
            post_type=state["post_type"],
            length=state["length"],
            post=post,
        )),
    ]
    response = llm.invoke(messages)
    formatted = response.content.strip()

    return {
        **state,
        "final_post": formatted,
    }
