import httpx

from ...fixtures.servers import *


def test_uvicorn_server(simple_uvicorn_server):
    response = httpx.get('http://127.0.0.1:8812/test-url')
    response_data = response.json()

    assert response.status_code == 499
    assert response_data.get('success') == False
