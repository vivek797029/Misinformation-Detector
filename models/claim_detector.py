import spacy

# Load spaCy model (ensure you run: python -m spacy download en_core_web_sm)
nlp = spacy.load("en_core_web_sm")

def extract_claims(text: str):
    """
    Simple claim extractor:
    - Splits into sentences
    - Keeps sentences that have a subject + verb and are longer than 6 words
    - Returns up to 6 claims
    """
    if not text or text.strip() == "":
        return []
    doc = nlp(text)
    claims = []
    for sent in doc.sents:
        words = sent.text.strip()
        if len(words.split()) < 6:
            continue
        # heuristic: sentence contains a nominal subject and a verb
        has_nsubj = any(tok.dep_ in ("nsubj", "nsubjpass") for tok in sent)
        has_verb = any(tok.pos_ == "VERB" for tok in sent)
        if has_nsubj and has_verb:
            claims.append(words)
    # fallback: if none found, split by newline and return first lines
    if not claims:
        lines = [l.strip() for l in text.splitlines() if l.strip()]
        return lines[:6]
    return claims[:6]
