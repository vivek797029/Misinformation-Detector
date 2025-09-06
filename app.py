import os
import base64
import tempfile
from fastapi import FastAPI, Request, UploadFile, Form, File
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from models.claim_detector import extract_claims
from services.factcheck import fact_check
from services.media_check import check_image
from services.score import credibility_score

import newspaper

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "result": None})


@app.post("/analyze", response_class=HTMLResponse)
async def analyze(request: Request,
                  url: str = Form(None),
                  text: str = Form(None),
                  file: UploadFile | None = File(None)):
    content = ""
    image_info = None
    image_b64 = None

    # 1) If URL provided, extract article text
    if url:
        try:
            article = newspaper.Article(url)
            article.download()
            article.parse()
            content = article.text
        except Exception as e:
            content = ""
    
    # 2) If text provided, use it
    if text:
        content = text

    # 3) If an image is uploaded, save temp and run media check
    if file:
        suffix = os.path.splitext(file.filename)[1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name
        # Media check
        image_info = check_image(tmp_path)
        # Convert to base64 for preview
        with open(tmp_path, "rb") as f:
            image_b64 = base64.b64encode(f.read()).decode("utf-8")
        # remove temp file
        try:
            os.remove(tmp_path)
        except:
            pass

    # 4) Extract claims
    claims = extract_claims(content)

    # 5) Fact-check each claim
    results = []
    for c in claims:
        fc = fact_check(c)
        score = credibility_score(fc, image_info)
        results.append({
            "claim": c,
            "fact": fc,
            "score": score
        })

    return templates.TemplateResponse("index.html", {
        "request": request,
        "result": results,
        "image_info": image_info,
        "image_b64": image_b64,
        "input_text": content[:400]
    })
