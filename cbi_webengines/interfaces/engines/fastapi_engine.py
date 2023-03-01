from typing import Any

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from cbi_ddd.repositories import SettingsRepository

from .engine import Engine
from ..settings import BaseEngineAppSettings


class FastAPIEngine(Engine):
    @classmethod
    def create_engine_app(cls) -> Any:
        config: BaseEngineAppSettings = SettingsRepository.get_config()

        app = FastAPI()

        # Middleware
        app.add_middleware(CORSMiddleware,
            allow_origins=config.cors.allow_origins,
            allow_credentials=config.cors.allow_credentials,
            allow_methods=config.cors.allow_methods,
            allow_headers=config.cors.allow_headers,
        )

        # Handlers
        app.exception_handler(StarletteHTTPException)(cls.error_handler)
        app.get('/status')(cls.status_handler)

        return app
    
    @classmethod
    def status_handler(cls, request: Request) -> JSONResponse:
        return JSONResponse(
            content={
                'success': True,
                'result': None,
                'error': None,
            }
        )

    @classmethod
    def error_handler(cls, request, exc):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                'success': False,
                'result': None,
                'error': {
                    'status_code': exc.status_code,
                    'message': str(exc.detail),
                }
            }
        )
