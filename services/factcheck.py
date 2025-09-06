import os
import requests
from sentence_transformers import SentenceTransformer, util

# load small/speedy model (cached)
EMBED_MODEL_NAME = "all-MiniLM-L6-v2"
_embed_model = None

def _get_embed_model():
    global _embed_model
    if _embed_model is None:
        _embed_model = SentenceTransformer(EMBED_MODEL_NAME)
    return _embed_model

# Demo “known claims” DB (small)
_DEMO_CLAIMS = [
    {"claim": "Vaccines cause autism", "rating": "False", "source": "https://www.who.int/news-room/qa-detail/vaccines-and-autism"},
    {"claim": "5G networks spread COVID-19", "rating": "False", "source": "https://www.bbc.com/news/technology-52085768"},
    {"claim": "Drinking water can cure diabetes", "rating": "False", "source": "https://healthinformation.org"},
    {"claim": "Eating carrots improves night vision", "rating": "Partly True", "source": "https://www.aao.org/eye-health/tips-prevention/eyes-nutrition"},
    {"claim": "The vaccine contains microchips", "rating": "False", "source": "https://fullfact.org"},
    {"claim": "Climate change is primarily caused by human activity", "rating": "True", "source": "https://www.ipcc.ch"}
]

API_URL = "https://factchecktools.googleapis.com/v1alpha1/claims:search"
API_KEY = os.getenv("GOOGLE_FC_API_KEY")  # optional

def _query_google_factcheck(claim_text):
    if not API_KEY:
        return None
    try:
        params = {"query": claim_text, "key": API_KEY}
        r = requests.get(API_URL, params=params, timeout=6)
        r.raise_for_status()
        res = r.json()
        if "claims" in res and len(res["claims"])>0:
            c = res["claims"][0]
            review = c.get("claimReview", [{}])[0]
            return {
                "claim": c.get("text"),
                "rating": review.get("textualRating", "Unverified"),
                "source": review.get("url"),
                "method": "google_api"
            }
    except Exception:
        return None
    return None

def _semantic_match_demo(claim_text):
    model = _get_embed_model()
    query_emb = model.encode(claim_text, convert_to_tensor=True)
    candidates = [d["claim"] for d in _DEMO_CLAIMS]
    cand_embs = model.encode(candidates, convert_to_tensor=True)
    scores = util.pytorch_cos_sim(query_emb, cand_embs)[0]
    best_idx = int(scores.argmax())
    best_score = float(scores[best_idx])
    best = _DEMO_CLAIMS[best_idx]
    return {
        "claim": best["claim"],
        "rating": best["rating"],
        "source": best["source"],
        "score": best_score,
        "method": "demo_semantic"
    }

def fact_check(claim_text):
    """Primary interface:
       - Try Google FactCheck (if key set)
       - Otherwise return nearest demo claim using semantic similarity
    """
    # 1) Try real API
    google = _query_google_factcheck(claim_text)
    if google:
        return google

    # 2) Fallback: semantic match to demo DB
    demo = _semantic_match_demo(claim_text)
    # Only accept matches with high confidence; otherwise return Unverified
    if demo["score"] >= 0.55:
        return {"claim": demo["claim"], "rating": demo["rating"], "source": demo["source"], "match_score": demo["score"], "method": demo["method"]}
    else:
        return {"claim": claim_text, "rating": "Unverified", "source": None, "match_score": demo["score"], "method": "none"}
