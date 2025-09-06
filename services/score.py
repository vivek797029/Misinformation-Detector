def _rating_to_score(rating: str):
    if not rating:
        return 50
    r = rating.lower()
    if "true" in r:
        return 90
    if "false" in r:
        return 15
    if "partly" in r or "misleading" in r:
        return 45
    if "unverified" in r or "none" in r:
        return 55
    return 50

def credibility_score(fact_result: dict, image_info: dict | None = None):
    base = _rating_to_score(fact_result.get("rating", "Unverified"))
    # If fact_result includes a match_score from semantic matching, adjust slightly
    match_adj = 0
    ms = fact_result.get("match_score")
    if ms:
        # boost confidence slightly if match is strong
        match_adj = int((ms - 0.5) * 20)  # rough mapping
    score = base + match_adj

    # if there's an image suspicion, reduce score proportionally
    if image_info and image_info.get("suspicion_score") is not None:
        sus = image_info["suspicion_score"]
        score = score - int(sus * 0.5)  # weight
    # clamp 0..100
    score = max(0, min(100, score))
    return score
