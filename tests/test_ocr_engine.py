import io
import pytest
from PIL import Image
from app.ai.ocr_engine import extract_ocr_from_image


def test_extract_ocr_from_image():
    img = Image.new("RGB", (100, 100), color=(200, 200, 200))
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    
    res = extract_ocr_from_image(buf.getvalue())
    assert "ocr_text" in res
    assert "entities" in res
    assert res["human_review_required"] is True
