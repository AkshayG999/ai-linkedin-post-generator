from typing import TypedDict, List, Optional


class PostState(TypedDict, total=False):
    # User inputs
    keywords: str
    post_type: str
    length: str
    language: str

    # Research phase
    raw_search_results: List[dict]
    summarized_research: str

    # Planning phase
    audience_profile: str
    outline: str

    # Drafting phase
    drafts: List[str]

    # Evaluation / refinement
    current_draft: str
    evaluation_scores: dict        # {draft_index: {dimension: score, total: float}}
    critique: str
    iteration_count: int

    # Finalization
    final_post: str
