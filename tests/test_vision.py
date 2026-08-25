import io
import pytest
from PIL import Image
from app.utils.image_utils import validate_and_save_image
from app.ai.vision import classify_complaint_image


def create_dummy_image_bytes(color=(100, 100, 100), fmt="PNG"):
    img = Image.new("RGB", (100, 100), color=color)
    buf = io.BytesIO()
    img.save(buf, format=fmt)
    return buf.getvalue()


def test_image_validation_valid():
    img_bytes = create_dummy_image_bytes()
    res = validate_and_save_image(img_bytes, "test.png")
    assert res["valid"] is True
    assert res["file_name"].startswith("img_")
    assert res["width"] == 100


def test_image_validation_invalid_extension():
    img_bytes = create_dummy_image_bytes()
    res = validate_and_save_image(img_bytes, "test.exe")
    assert res["valid"] is False
    assert "Invalid extension" in res["error"]


def test_classify_complaint_image_dark_cleanliness():
    img_bytes = create_dummy_image_bytes(color=(30, 30, 30))
    res = classify_complaint_image(img_bytes)
    assert res["predicted_category"] == "Cleanliness"
    assert res["confidence"] > 0.50
