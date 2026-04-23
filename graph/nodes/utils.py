def get_best_draft_index(drafts: list, scores: dict) -> int:
    """Return the index of the highest-scoring draft."""
    best_index = 0
    best_total = -1.0
    for i in range(len(drafts)):
        entry = scores.get(i, {})
        total = float(entry.get("total", 0))
        if total > best_total:
            best_total = total
            best_index = i
    return best_index
