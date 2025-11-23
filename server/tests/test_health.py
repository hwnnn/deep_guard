import base64
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"

def test_face_swap_inference():
    # Create two tiny in-memory images
    from PIL import Image
    from io import BytesIO
    src = Image.new("RGB", (50, 50), color=(255, 0, 0))
    tgt = Image.new("RGB", (120, 80), color=(0, 255, 0))
    src_b = BytesIO(); src.save(src_b, format="JPEG")
    tgt_b = BytesIO(); tgt.save(tgt_b, format="JPEG")
    files = {
        "source": ("src.jpg", src_b.getvalue(), "image/jpeg"),
        "target": ("tgt.jpg", tgt_b.getvalue(), "image/jpeg"),
    }
    r = client.post("/api/inference/face-swap", files=files)
    assert r.status_code == 200
    data = r.json()
    assert "result_image_base64" in data
    assert data["status"] == "success"
    # basic sanity: decodable
    base64.b64decode(data["result_image_base64"])  # raises if invalid
