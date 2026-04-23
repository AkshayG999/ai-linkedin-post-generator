HASHTAG_SYSTEM = (
    "You are a LinkedIn hashtag strategy expert. You select optimal hashtags that maximize "
    "post reach and relevance."
)

HASHTAG_HUMAN = """
For a LinkedIn post about "{keywords}" (post type: {post_type}), suggest exactly 5 optimal hashtags.

Criteria:
- 1 high-volume hashtag (very broad, >500k followers, e.g. #Leadership, #AI, #Marketing)
- 2 mid-tier hashtags (topic-specific, 50k–200k followers)
- 2 niche hashtags (highly specific to the topic, smaller but highly engaged audiences)

Return ONLY a JSON object in this exact format (no markdown, no explanation):
{{
  "hashtags": ["#Tag1", "#Tag2", "#Tag3", "#Tag4", "#Tag5"],
  "rationale": "<one sentence explaining the hashtag mix strategy>"
}}
"""
