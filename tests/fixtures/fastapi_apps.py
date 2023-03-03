import pytest
import time

from multiprocessing import Process
from typing import List

from fastapi.testclient import TestClient
from pydantic import BaseModel

from cbi_webengines.interfaces import (
    servers,
    Router,
    Handler,
    Header,
    Middleware,
    DataRequest,
    DataResponse,
)
from cbi_webengines.repositories import (
    ApplicationRepository,
    engines,
)


class AppHandlerRequestData(BaseModel):
    tests: List[str] = []


class AppHandlerResponseData(BaseModel):
    request_tests: List[str]
    response_tests: List[str]
    headers: List[Header]


class AppMiddleware1(Middleware):
    async def process_request(self, request: DataRequest) -> DataRequest:
        if not request.data:
            request.data = AppHandlerRequestData()
        request.data.tests.append('tested_AppMiddleware1')
        return request
    
    async def process_response(self, response: DataResponse) -> DataResponse:
        response.result.response_tests.append('tested_AppMiddleware1')
        return await super().process_response(response)
    

class AppMiddleware2(Middleware):
    async def process_request(self, request: DataRequest) -> DataRequest:
        request.data.tests.append('tested_AppMiddleware2')
        return request
    
    async def process_response(self, response: DataResponse) -> DataResponse:
        response.result.response_tests.append('tested_AppMiddleware2')
        return await super().process_response(response)
    

class AppMiddleware3(Middleware):
    async def process_request(self, request: DataRequest) -> DataRequest:
        request.data.tests.append('tested_AppMiddleware3')
        return request
    
    async def process_response(self, response: DataResponse) -> DataResponse:
        response.result.response_tests.append('tested_AppMiddleware3')
        return await super().process_response(response)
    

class RouterMiddleware1(Middleware):
    async def process_request(self, request: DataRequest) -> DataRequest:
        request.data.tests.append('tested_RouterMiddleware1')
        return request
    
    async def process_response(self, response: DataResponse) -> DataResponse:
        response.result.response_tests.append('tested_RouterMiddleware1')
        return await super().process_response(response)
    

class RouterMiddleware2(Middleware):
    async def process_request(self, request: DataRequest) -> DataRequest:
        request.data.tests.append('tested_RouterMiddleware2')
        return request
    
    async def process_response(self, response: DataResponse) -> DataResponse:
        response.result.response_tests.append('tested_RouterMiddleware2')
        return await super().process_response(response)
    

class AddHeaderMiddleware(Middleware):
    async def process_request(self, request: DataRequest) -> DataRequest:
        request.headers.append(Header(
            name='TEST-HEADER-3', value='test3',
        ))
        return request


class RouteHandler(Handler):
    url_prefix = '/test_route'
    request_data = AppHandlerRequestData
    
    async def do(self, request: DataRequest) -> DataResponse:
        print(request.data)
        return DataResponse(
            result=AppHandlerResponseData(
                request_tests=request.data.tests,
                response_tests=[
                    'handle_RouteHandler',
                ],
                headers=[],
            ),
        )
    

class ExtractHeadersHandler(Handler):
    url_prefix = '/extract_headers'
    method = 'GET'

    async def do(self, request: DataRequest) -> DataResponse:
        return DataResponse(
            result=AppHandlerResponseData(
                request_tests=[],
                response_tests=[],
                headers=request.headers,
            ),
        )


class RaiseExceptionHandler(Handler):
    url_prefix = '/raise_exception'
    method = 'GET'

    async def do(self, request: DataRequest) -> DataResponse:
        raise Exception('Test exception')


@pytest.fixture()
def simple_fastapi_app():
    return ApplicationRepository.create_application(
        url_prefix='/',
        server=servers.UvicornServer,
        engine=engines.FastAPIEngineRepository,
    )

@pytest.fixture()
def fastapi_app():
    app = ApplicationRepository.create_application(
        url_prefix='',
        server=servers.UvicornServer,
        engine=engines.FastAPIEngineRepository,
    )

    app.add_middleware(AppMiddleware1)
    app.add_middleware(AppMiddleware2)
    app.add_middleware(AppMiddleware3)

    test_router = Router('/test_router')
    test_router.add_middleware(RouterMiddleware1)
    test_router.add_middleware(RouterMiddleware2)
    test_router.add_middleware(AddHeaderMiddleware)

    test_router.connect_handler(RouteHandler)
    test_router.connect_handler(ExtractHeadersHandler)
    test_router.connect_handler(RaiseExceptionHandler)

    app.connect_router(test_router)

    return app

@pytest.fixture()
def simple_test_client(simple_fastapi_app):
    return TestClient(simple_fastapi_app.get_engine_app())

@pytest.fixture()
def test_client(fastapi_app):
    return TestClient(fastapi_app.get_engine_app())

def run_server(app):
    from cbi_ddd.repositories import SettingsRepository
    from cbi_webengines.interfaces.settings import BaseEngineAppSettings

    SettingsRepository.settings_model = BaseEngineAppSettings

    app.serve()

@pytest.fixture()
def simple_uvicorn_proc(simple_fastapi_app):
    proc = Process(
        target=run_server,
        args=(simple_fastapi_app,),
        daemon=True
    )
    proc.start()
    time.sleep(1)
    yield
    proc.kill()
