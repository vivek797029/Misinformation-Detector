import os
from PIL import Image, ExifTags

def _extract_exif(img):
    try:
        exif = img._getexif()
        if not exif:
            return None
        data = {}
        for k, v in exif.items():
            tag = ExifTags.TAGS.get(k, k)
            data[tag] = v
        return data
    except Exception:
        return None

def check_image(path: str):
    """
    Basic checks:
      - Can we open the image?
      - Does it contain EXIF metadata?
      - File size, dimensions heuristics
    Returns a dictionary with verdict and details.
    """
    try:
        img = Image.open(path)
        width, height = img.size
        exif = _extract_exif(img)
        size_bytes = os.path.getsize(path)

        suspicion = 0
        reasons = []
        # No metadata may indicate stripping (but not proof)
        if not exif:
            suspicion += 30
            reasons.append("No EXIF metadata found")
        # Very small file size may indicate heavy compression or generated thumbnail
        if size_bytes < 50_000:
            suspicion += 10
            reasons.append("Small file size")
        # Very small dimensions
        if width < 400 or height < 400:
            suspicion += 10
            reasons.append("Low resolution")
        # Unusual aspect or huge size (not suspicious by itself)
        verdict = "Likely Authentic"
        if suspicion >= 40:
            verdict = "Possibly AI-generated / metadata stripped"
        elif suspicion >= 20:
            verdict = "Suspicious — review manually"

        return {
            "status": "checked",
            "verdict": verdict,
            "suspicion_score": suspicion,
            "reasons": reasons,
            "width": width,
            "height": height,
            "size_bytes": size_bytes,
            "has_exif": bool(exif)
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
