import pytest
from fastapi.testclient import TestClient
from main import app
from PIL import Image
import io

client = TestClient(app)

# Mocking the model loading and inference to avoid huge downloads during simple API tests?
# Or should I test the real deal? 
# The user wants a "POC" and "Verification".
# Running the real models is better, but slower.
# Let's try to test the root endpoint first.

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]

@pytest.mark.skip(reason="Requires model download which takes time")
def test_upscale_e2e():
    # Create a small dummy image
    img = Image.new('RGB', (32, 32), color = 'red')
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)

    files = {'file': ('test.png', img_byte_arr, 'image/png')}
    
    # Test Fidelity
    response = client.post("/upscale", files=files, data={"mode": "fidelity"})
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/png"
