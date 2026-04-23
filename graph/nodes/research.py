import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from exa_py import Exa

from graph.state import PostState
from prompts.research_prompt import RESEARCH_SYSTEM, RESEARCH_HUMAN


def research_node(state: PostState) -> PostState:
    """
    Node 1 – Research
    Calls Exa to retrieve articles then uses an LLM to distil a research brief.
    """
    keywords = state["keywords"]

    # --- Web search via Exa ---
    raw_results = []
    summarized_research = ""

    metaphor_key = os.getenv("METAPHOR_API_KEY")
    if metaphor_key:
        try:
            exa = Exa(metaphor_key)
            response = exa.search_and_contents(
                keywords, use_autoprompt=True, num_results=5
            )
            raw_results = [
                {
                    "title": r.title or "",
                    "url": r.url or "",
                    "text": (r.text or "")[:1500],  # cap per-result text
                }
                for r in response.results
                if r
            ]
        except Exception:
            raw_results = []

    # --- LLM research summarisation ---
    raw_text = "\n\n".join(
        f"Title: {r['title']}\nURL: {r['url']}\nContent: {r['text']}"
        for r in raw_results
    ) if raw_results else f"No search results available. Please write based on your knowledge of: {keywords}"

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)
    messages = [
        SystemMessage(content=RESEARCH_SYSTEM),
        HumanMessage(content=RESEARCH_HUMAN.format(
            keywords=keywords,
            raw_results=raw_text,
        )),
    ]
    response = llm.invoke(messages)
    summarized_research = response.content.strip()

    return {
        **state,
        "raw_search_results": raw_results,
        "summarized_research": summarized_research,
    }
