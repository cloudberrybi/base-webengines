import pytest
import asyncio
import time

from multiprocessing import Process

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from cbi_webengines.interfaces.servers import UvicornServer


def run_fastapi_server(port):
    def handler(request: Request):
        return JSONResponse(
            status_code=499,
            content={
                'success': False,
            }
        )

    app = FastAPI()
    app.get('/test-url')(handler)

    asyncio.run(
        UvicornServer.async_serve(
            app=app,
            port=port,
        )
    )

@pytest.fixture()
def simple_uvicorn_server():
    proc = Process(
        target=run_fastapi_server,
        args=(8812,),
        daemon=True
    )
    proc.start()
    time.sleep(1)
    yield
    proc.kill()
