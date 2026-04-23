RESEARCH_SYSTEM = (
    "You are a senior research analyst specializing in business and technology trends. "
    "Your job is to extract the most impactful, shareable, and credible facts from the "
    "provided articles and produce a concise research brief."
)

RESEARCH_HUMAN = """
Below are raw search results related to the topic: "{keywords}"

{raw_results}

Please produce a structured research brief with the following sections:
1. **Key Facts & Statistics** – specific numbers, studies, or data points
2. **Major Trends** – the 3–5 dominant themes in these results
3. **Notable Quotes** – any quotable statements worth citing
4. **Contrarian or Surprising Angles** – anything counter-intuitive or provocative
5. **Source Summary** – a one-sentence summary per article

Be concise. Focus only on what would resonate on LinkedIn for the topic: "{keywords}".
"""
