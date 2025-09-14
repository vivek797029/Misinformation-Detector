import os
import base64
import tempfile
from pathlib import Path  # ✅ cross-platform paths

from fastapi import FastAPI, Request, UploadFile, Form, File
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from models.claim_detector import extract_claims
from services.factcheck import fact_check
from services.media_check import check_image
from services.score import credibility_score

import newspaper

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

app = FastAPI()
app.mount(
    "/static",
    StaticFiles(directory=str(BASE_DIR / "static")),
    name="static"
)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "result": None})


@app.post("/analyze", response_class=HTMLResponse)
async def analyze(
    request: Request,
    url: str = Form(None),
    text: str = Form(None),
    file: UploadFile | None = File(None)
):
    content = ""
    image_info = None
    image_b64 = None

    if url:
        try:
            article = newspaper.Article(url)
            article.download()
            article.parse()
            content = article.text
        except Exception:
            content = ""

    if text:
        content = text

    if file:
        suffix = Path(file.filename).suffix
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(await file.read())
            tmp_path = Path(tmp.name)

        image_info = check_image(str(tmp_path))

        with open(tmp_path, "rb") as f:
            image_b64 = base64.b64encode(f.read()).decode("utf-8")

        try:
            tmp_path.unlink(missing_ok=True)
        except Exception:
            pass

    claims = extract_claims(content)

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
