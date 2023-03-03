import httpx

from ...fixtures.fastapi_apps import *


def test_simple_fastapi_app(simple_test_client):
    response = simple_test_client.get('/status')
    response_data = response.json()

    assert response.status_code == 200
    assert response_data.get('success') == True

def test_fastapi_route(test_client):
    response = test_client.post('/test_router/test_route')
    response_data = response.json()

    assert response.status_code == 200
    assert response_data == {
        'status_code': 200,
        'success': True,
        'result': {
            'request_tests': [
                'tested_AppMiddleware1',
                'tested_AppMiddleware2',
                'tested_AppMiddleware3',
                'tested_RouterMiddleware1',
                'tested_RouterMiddleware2'
            ],
            'response_tests': [
                'handle_RouteHandler',
                'tested_RouterMiddleware2',
                'tested_RouterMiddleware1',
                'tested_AppMiddleware3',
                'tested_AppMiddleware2',
                'tested_AppMiddleware1'
            ],
            'headers': [],
        },
        'error': None
    }

def test_extract_headers_route(test_client):
    response = test_client.get(
        '/test_router/extract_headers',
        headers={
            'Test-Header-1': 'test1',
            'test-header-2': 'test2'
        }
    )
    response_data = response.json()

    assert response.status_code == 200
    assert response_data == {
        'status_code': 200,
        'success': True,
        'result': {
            'request_tests': [],
            'response_tests': [
                'tested_RouterMiddleware2',
                'tested_RouterMiddleware1',
                'tested_AppMiddleware3',
                'tested_AppMiddleware2',
                'tested_AppMiddleware1'
            ],
            'headers': [
                {'name': 'HOST', 'value': 'testserver'},
                {'name': 'ACCEPT', 'value': '*/*'},
                {'name': 'ACCEPT-ENCODING', 'value': 'gzip, deflate'},
                {'name': 'CONNECTION', 'value': 'keep-alive'},
                {'name': 'USER-AGENT', 'value': 'testclient'},
                {'name': 'TEST-HEADER-1', 'value': 'test1'},
                {'name': 'TEST-HEADER-2', 'value': 'test2'},
                {'name': 'TEST-HEADER-3', 'value': 'test3'}
            ]
        },
        'error': None
    }

def test_raise_unknown_exception(test_client):
    response = test_client.get('/test_router/raise_exception')
    response_data = response.json()

    assert response.status_code == 400
    assert response_data == {
        'status_code': 400,
        'success': False,
        'result': None,
        'error': 'Test exception'
    }

def test_fastapi_unfound_route(test_client):
    response = test_client.get('/test_router/not_found')
    response_data = response.json()

    assert response.status_code == 404
    assert response_data == {
        'status_code': 404,
        'success': False,
        'result': None,
        'error': {
            'code': 'NOT_FOUND',
            'message': 'Unknown route',
            'args': {
                'path': '/test_router/not_found',
            }
        },
    }

def test_simple_uvicorn_server(simple_uvicorn_proc):
    response = httpx.get('http://127.0.0.1:8811/status')
    response_data = response.json()

    assert response.status_code == 200
    assert response_data.get('success') == True
