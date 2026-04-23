REFINER_SYSTEM = (
    "You are a LinkedIn post editor. Your job is to improve a draft post based on a "
    "specific critique while preserving everything that already works well."
)

REFINER_HUMAN = """
Below is a LinkedIn post draft and its quality critique. Rewrite the post to fix only the issues identified.

**Do NOT change** elements that scored 8 or above — preserve them exactly.
**Do improve** the weakest-scoring areas as described in the critique.
**Preserve** the author's voice, the core message, and the post structure.

**Current Draft:**
{current_draft}

**Quality Scores (out of 10):**
{scores_summary}

**Critique:**
{critique}

**Weak Dimensions to Fix (scored below 8):**
{weak_dimensions}

Return ONLY the improved post text with no commentary or preamble.
Keep all LinkedIn formatting rules: one sentence per line, emojis at section starts, 3–5 hashtags at end.
"""
