# Проверяем доступность главной ручки
import requests
import pytest
from src.settings import PREFIX


@pytest.mark.parametrize("url", [
    f"http://127.0.0.1:8000/{PREFIX}"
])
def test_empty_meme_array(url):
    response = requests.get(url)

    assert response.status_code == 200
