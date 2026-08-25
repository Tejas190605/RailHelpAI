import io
import pytest
from PIL import Image
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def create_dummy_image_bytes():
    img = Image.new("RGB", (100, 100), color=(100, 100, 100))
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def test_api_analyze_multimodal_text_only():
    res = client.post(
        "/api/v1/ai/analyze-multimodal",
        data={"text": "AC is not cooling in coach B4 seat 21."}
    )
    assert res.status_code == 200
    data = res.json()
    assert data["text_analysis"]["category"] == "Air Conditioning"


def test_api_analyze_multimodal_with_image():
    img_bytes = create_dummy_image_bytes()
    files = {"image": ("test.png", img_bytes, "image/png")}
    data = {"text": "Dirty coach floor in B4."}
    res = client.post("/api/v1/ai/analyze-multimodal", data=data, files=files)
    assert res.status_code == 200
    res_data = res.json()
    assert res_data["image_analysis"] is not None


def test_api_trends():
    res = client.get("/api/v1/analytics/trends")
    assert res.status_code == 200
    assert "category_trends" in res.json()


def test_api_recommendations():
    res = client.get("/api/v1/analytics/recommendations")
    assert res.status_code == 200
    assert isinstance(res.json(), list)


def test_api_risk():
    res = client.get("/api/v1/analytics/risk")
    assert res.status_code == 200
    assert "risk_index" in res.json()
