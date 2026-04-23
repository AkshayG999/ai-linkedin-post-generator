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

    # asyncio.run works whether or not there is an existing event loop at the
    # top level; Streamlit runs in a synchronous context so this is safe.
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # Running inside an existing loop (e.g. Jupyter / some ASGI hosts)
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as pool:
                future = pool.submit(asyncio.run, run_all())
                drafts = future.result()
        else:
            drafts = loop.run_until_complete(run_all())
    except RuntimeError:
        drafts = asyncio.run(run_all())

    return {
        **state,
        "drafts": list(drafts),
    }
