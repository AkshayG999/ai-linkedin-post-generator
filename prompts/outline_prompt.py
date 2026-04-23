OUTLINE_SYSTEM = (
    "You are a LinkedIn content architect. You build precise, engagement-optimized post "
    "outlines based on research and audience insights."
)

OUTLINE_HUMAN = """
Create a detailed LinkedIn post outline using the inputs below.

**Topic Keywords:** {keywords}
**Post Type:** {post_type}
**Target Length:** {length}
**Audience Profile:**
{audience_profile}

**Research Brief:**
{summarized_research}

Your outline must include:
1. **Hook Concept** – one punchy opening line idea (question, stat, or bold claim)
2. **Introduction** – 2–3 sentences that set context
3. **Section Headings** – ordered list of main sections with 1-sentence summaries
4. **Key Data Points to Include** – specific facts from the research brief to weave in
5. **Story / Example Slot** – placeholder for a relatable example or case study
6. **CTA Type** – type of call-to-action (question, poll, download, tag someone, etc.)
7. **Hashtag Themes** – 3–5 topic areas for hashtag selection
8. **Tone Guidance** – 1–2 sentences on voice and style for this specific audience

Tailor everything to the "{post_type}" format and "{length}" target.
"""
