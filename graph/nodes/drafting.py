import asyncio
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

from graph.state import PostState
from prompts.draft_prompt import DRAFT_SYSTEM, DRAFT_HUMAN, STYLE_ANGLES


async def _generate_draft(llm: ChatOpenAI, style_angle: str, state: PostState) -> str:
    messages = [
        SystemMessage(content=DRAFT_SYSTEM),
        HumanMessage(content=DRAFT_HUMAN.format(
            style_angle=style_angle,
            post_type=state["post_type"],
            length=state["length"],
            language=state["language"],
            outline=state["outline"],
            summarized_research=state["summarized_research"],
            audience_profile=state["audience_profile"],
        )),
    ]
    response = await llm.ainvoke(messages)
    return response.content.strip()


def multi_draft_node(state: PostState) -> PostState:
    """
    Node 4 – Multi-Draft
    Generates 3 parallel draft variants (story, data, contrarian) using gpt-4o.
    """
    llm = ChatOpenAI(model="gpt-4o", temperature=0.8)

    async def run_all():
        return await asyncio.gather(*[
            _generate_draft(llm, angle, state) for angle in STYLE_ANGLES
        ])

    # asyncio.run() creates a new event loop each time, which is the safest
    # approach in a synchronous context (Streamlit).
    # If a loop is already running (e.g. Jupyter / some ASGI hosts), fall back
    # to running in a thread pool to avoid "cannot run nested event loop" errors.
    try:
        asyncio.get_running_loop()
        # A loop is already running — delegate to a thread with its own loop.
        import concurrent.futures
        with concurrent.futures.ThreadPoolExecutor() as pool:
            future = pool.submit(asyncio.run, run_all())
            drafts = future.result()
    except RuntimeError:
        # No running loop — safe to call asyncio.run() directly.
        drafts = asyncio.run(run_all())

    return {
        **state,
        "drafts": list(drafts),
    }
