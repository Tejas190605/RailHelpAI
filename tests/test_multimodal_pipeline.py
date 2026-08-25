import io
import pytest
from PIL import Image
from app.ai.multimodal_pipeline import analyze_multimodal_complaint


def create_dummy_image_bytes(color=(100, 100, 100)):
    img = Image.new("RGB", (100, 100), color=color)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def test_multimodal_text_only():
    res = analyze_multimodal_complaint("AC is not working in coach B4 seat 21.")
    assert res["text_analysis"]["category"] == "Air Conditioning"
    assert res["image_analysis"] is None
    assert res["fusion"]["conflict_detected"] is False


def test_multimodal_with_image():
    img_bytes = create_dummy_image_bytes(color=(30, 30, 30))  # Dark image -> Cleanliness
    res = analyze_multimodal_complaint("AC is not working in coach B4.", image_bytes=img_bytes, original_filename="test.png")
    assert res["image_analysis"] is not None
    assert res["fusion"]["conflict_detected"] is True  # AC text vs Cleanliness image
    assert res["fusion"]["human_review_required"] is True
