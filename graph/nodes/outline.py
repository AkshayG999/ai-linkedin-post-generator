from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

from graph.state import PostState
from prompts.outline_prompt import OUTLINE_SYSTEM, OUTLINE_HUMAN


def outline_node(state: PostState) -> PostState:
    """
    Node 3 – Outline
    Builds a structured post outline from research + audience profile.
    """
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.4)
    messages = [
        SystemMessage(content=OUTLINE_SYSTEM),
        HumanMessage(content=OUTLINE_HUMAN.format(
            keywords=state["keywords"],
            post_type=state["post_type"],
            length=state["length"],
            audience_profile=state["audience_profile"],
            summarized_research=state["summarized_research"],
        )),
    ]
    response = llm.invoke(messages)
    return {
        **state,
        "outline": response.content.strip(),
    }
