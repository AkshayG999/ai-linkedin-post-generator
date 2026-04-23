from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

from graph.state import PostState
from prompts.audience_prompt import AUDIENCE_SYSTEM, AUDIENCE_HUMAN


def audience_profiler_node(state: PostState) -> PostState:
    """
    Node 2 – Audience Profiler
    Identifies the ideal LinkedIn audience segment for the post.
    """
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.4)
    messages = [
        SystemMessage(content=AUDIENCE_SYSTEM),
        HumanMessage(content=AUDIENCE_HUMAN.format(
            keywords=state["keywords"],
            post_type=state["post_type"],
            language=state["language"],
        )),
    ]
    response = llm.invoke(messages)
    return {
        **state,
        "audience_profile": response.content.strip(),
    }
