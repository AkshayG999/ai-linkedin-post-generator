DRAFT_SYSTEM = (
    "You are an expert LinkedIn content writer who creates high-engagement posts. "
    "Write in the style specified, following the outline and research provided."
)

DRAFT_HUMAN = """
Write a complete LinkedIn post based on the following inputs.

**Style Angle:** {style_angle}
**Post Type:** {post_type}
**Target Length:** {length}
**Language:** {language}

**Outline:**
{outline}

**Research Brief:**
{summarized_research}

**Audience Profile:**
{audience_profile}

Style Angle Descriptions:
- "story-driven": Open with a personal or relatable narrative. Use "I" or "We" voice. Build tension then resolve.
- "data-driven": Lead with a compelling statistic. Use numbered evidence. Be precise and cite figures.
- "contrarian": Open with a bold, counter-intuitive claim. Challenge common wisdom. Be provocative but constructive.

LinkedIn Formatting Rules (MUST follow):
- Each sentence or short thought on its own line
- Use emojis strategically at section starts and the hook (not in every sentence)
- 3–5 relevant hashtags at the end only
- No URLs in the body (mention "link in comments" if needed)
- End with an engagement question or clear CTA

Write the FULL post now in {language}.
"""

STYLE_ANGLES = ["story-driven", "data-driven", "contrarian"]
