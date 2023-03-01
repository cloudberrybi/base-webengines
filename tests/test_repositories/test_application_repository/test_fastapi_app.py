import httpx

from ...fixtures.fastapi_apps import *


def test_simple_fastapi_app(simple_test_client):
    response = simple_test_client.get('/status')
    response_data = response.json()

    assert response.status_code == 200
    assert response_data.get('success') == True

def test_fastapi_route(test_client):
    response = test_client.get('/test_router/test_route')
    response_data = response.json()

    assert response.status_code == 200
    assert response_data == {
        'success': True,
        'result': {
            'test': 123,
        },
        'error': None,
    }

def test_fastapi_unfound_route(test_client):
    response = test_client.get('/test_router/not_found')
    response_data = response.json()

    assert response.status_code == 404
    assert response_data == {
        'success': False,
        'result': None,
        'error': {
            'code': 'NOT_FOUND',
            'message': 'Unknown route',
            'args': {
                'route': '/test_router/not_found',
            }
        },
    }

def test_simple_uvicorn_server(simple_uvicorn_proc):
    response = httpx.get('http://127.0.0.1:8811/status')
    response_data = response.json()

    assert response.status_code == 200
    assert response_data.get('success') == True
