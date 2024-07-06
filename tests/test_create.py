# Проверяем создание объекта в БД
from settings import PREFIX
import pytest
import requests
import tempfile

API_URL = f"http://127.0.0.1:8000/{PREFIX}/"


@pytest.fixture(scope="module")
def temp_image():
    temp_file = tempfile.NamedTemporaryFile(suffix=".jpg")
    return temp_file


@pytest.mark.asyncio
async def test_create_meme(temp_image):
    data = {
        "description": None
    }

    with open(temp_image.name, 'rb') as image_file:
        files = {"image": ("temp_image.jpg", image_file, "image/jpeg")}
        response = requests.post(f"{API_URL}", data=data, files=files)

    assert response.status_code == 200
    assert 'id' in response.json()

    # Проверяем, что мем создался
    created_meme_id = response.json()['id']
    created_meme = requests.get(f"{API_URL}{created_meme_id}/")
    assert created_meme.status_code == 200
    assert 'image_path' in created_meme.json()
    assert 'emp_image.jpg' in created_meme.json()['image_path']
    assert created_meme.json()['description'] == data['description']
