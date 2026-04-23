EVALUATOR_SYSTEM = (
    "You are a LinkedIn content quality evaluator. You score posts on a structured rubric "
    "and provide specific, actionable critique. You MUST return valid JSON only."
)

EVALUATOR_HUMAN = """
Evaluate the following LinkedIn post draft for a post about "{keywords}" targeting this audience:
{audience_profile}

**DRAFT:**
{draft}

Score this post on each dimension from 0 to 10, where 10 is perfect:

1. **hook_strength** – Does the first line compel the reader to continue? Is it surprising, emotional, or thought-provoking?
2. **engagement_potential** – Does the post invite reactions, comments, or shares? Does it include questions or provocative statements?
3. **linkedin_algorithm_score** – Proper formatting (line breaks), ideal length for the post type, 3–5 hashtags at end, no external links in body?
4. **eeat_score** – Does it demonstrate Experience, Expertise, Authoritativeness, and Trustworthiness? Are claims backed by data?
5. **readability** – Short sentences, clear structure, easy to skim on mobile, appropriate vocabulary for the audience?
6. **cta_quality** – Is the call-to-action clear, specific, and motivating? Does it give readers a reason to engage?

Return ONLY a JSON object in this exact format (no markdown, no explanation):
{{
  "hook_strength": <0-10>,
  "engagement_potential": <0-10>,
  "linkedin_algorithm_score": <0-10>,
  "eeat_score": <0-10>,
  "readability": <0-10>,
  "cta_quality": <0-10>,
  "total": <sum of all six scores>,
  "critique": "<2-3 sentences identifying the weakest aspects and how to fix them>"
}}
"""
