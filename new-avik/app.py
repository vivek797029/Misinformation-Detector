import os
import base64
import tempfile
import statistics
from fastapi import FastAPI, Request, UploadFile, Form, File
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import newspaper

# --- Mock/Placeholder Imports ---
# These placeholder functions mimic the behavior of your actual analysis modules.
# Replace these with your actual imports:
# from models.claim_detector import extract_claims
# from services.factcheck import fact_check
# from services.media_check import check_image
# from services.score import credibility_score

def extract_claims(text: str):
    if not text: return []
    return [s for s in text.split('.') if len(s.strip()) > 10][:5]

def fact_check(claim: str):
    if "true" in claim.lower(): return {"rating": "True", "source": "http://example-source.com"}
    if "false" in claim.lower(): return {"rating": "False", "source": "http://example-source.com"}
    return {"rating": "Unverified", "source": None}

def check_image(path: str):
    return {"verdict": "Possibly AI-generated", "suspicion_score": 45, "reasons": ["No EXIF metadata"], "has_exif": False}

def credibility_score(fact_result: dict, image_info: dict = None):
    base = {"True": 90, "False": 10, "Unverified": 50}.get(fact_result["rating"], 50)
    if image_info: base -= image_info['suspicion_score'] * 0.2
    return max(0, min(100, int(base)))
# --- End of Mock/Placeholder Imports ---


# --- App Setup ---
app = FastAPI()

# Ensure required directories exist to prevent startup errors
os.makedirs("templates", exist_ok=True)
os.makedirs("static", exist_ok=True)

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


# --- Helper Functions ---
async def handle_image_upload(file: UploadFile):
    if not file or not file.filename:
        return None, None

    image_info = None
    image_b64 = None
    tmp_path = ""
    
    try:
        suffix = os.path.splitext(file.filename)[1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            file_content = await file.read()
            tmp.write(file_content)
            tmp_path = tmp.name
        
        image_info = check_image(tmp_path)
        image_b64 = base64.b64encode(file_content).decode("utf-8")
    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)
            
    return image_info, image_b64


# --- API Endpoints ---
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Serves the main landing page."""
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/analyze", response_class=HTMLResponse)
async def analyze(request: Request,
                  url: str = Form(None),
                  text: str = Form(None),
                  file: UploadFile | None = File(None)):
    """Analyzes user-provided input and serves the results page."""
    content = ""
    input_source = "N/A"

    if url:
        input_source = url
        try:
            article = newspaper.Article(url)
            article.download()
            article.parse()
            content = article.text or "Article text could not be extracted."
        except Exception:
            content = f"Could not retrieve or parse the article from: {url}"
    elif text:
        content = text
        input_source = f"Text starting with: \"{content[:70]}...\""

    image_info, image_b64 = await handle_image_upload(file)
    if image_info and input_source == "N/A":
        input_source = f"Image: {file.filename if file else 'Uploaded Image'}"

    claims = extract_claims(content)
    results = []
    for c in claims:
        fact_check_result = fact_check(c)
        claim_score = credibility_score(fact_check_result, image_info)
        results.append({
            "claim": c,
            "fact": fact_check_result,
            "score": claim_score
        })

    text_based_score = round(statistics.mean([r['score'] for r in results])) if results else None
    image_based_score = 100 - image_info['suspicion_score'] if image_info else None
    
    if text_based_score is not None and image_based_score is not None:
        overall_score = round((text_based_score * 0.7) + (image_based_score * 0.3))
    else:
        overall_score = text_based_score or image_based_score or 0

    verdict = "Could Not Determine"
    if overall_score > 0:
        if overall_score >= 75: verdict = "Low Credibility Risk"
        elif overall_score >= 50: verdict = "Medium Credibility Risk"
        else: verdict = "High Credibility Risk"

    return templates.TemplateResponse("results.html", {
        "request": request, "results": results, "image_info": image_info,
        "image_b64": image_b64, "input_source": input_source,
        "overall_score": overall_score, "verdict": verdict,
    })

