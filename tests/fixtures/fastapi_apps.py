import pytest
import time

from multiprocessing import Process

from fastapi.testclient import TestClient

from cbi_webengines.interfaces import (
    engines,
    servers,
)
from cbi_webengines.repositories import ApplicationRepository


@pytest.fixture()
def simple_fastapi_app():
    return ApplicationRepository.create_application(
        url_prefix='/',
        server=servers.UvicornServer,
        engine=engines.FastAPIEngine,
    )

@pytest.fixture()
def fastapi_app():
    app = ApplicationRepository.create_application(
        url_prefix='/',
        server=servers.UvicornServer,
        engine=engines.FastAPIEngine,
    )

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
