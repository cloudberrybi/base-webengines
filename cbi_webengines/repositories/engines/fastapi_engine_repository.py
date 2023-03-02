from typing import Any

from fastapi import FastAPI, Request, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from cbi_ddd.repositories import SettingsRepository
from cbi_webengines.interfaces import (
    EngineRepository,
    DataRequest,
    DataResponse,
    Application,
    Handler,
    settings,
    errors,
)


class FastAPIEngineRepository(EngineRepository):
    @classmethod
    def create_engine_app(cls, application: Application) -> Any:
        config: settings.BaseEngineAppSettings = SettingsRepository.get_config()

        app = FastAPI()

        # Middleware
        app.add_middleware(CORSMiddleware,
            allow_origins=config.cors.allow_origins,
            allow_credentials=config.cors.allow_credentials,
            allow_methods=config.cors.allow_methods,
            allow_headers=config.cors.allow_headers,
        )

        async def exception_middleware(request: Request, call_next):
            try:
                response = await call_next(request)
            except Exception as ex:
                if isinstance(ex, errors.EngineError):
                    response = JSONResponse(
                        status_code=ex.status_code,
                        content=DataResponse(
                            success=False,
                            status_code=ex.status_code,
                            result=None,
                            error=ex.data,
                        ).dict(),
                    )

            return response

        app.middleware("http")(exception_middleware)

        for router_item in application.routers:
            router = APIRouter()

            for handler_cls in router_item.handlers:
                async def handler(request: Request):
                    response = await handler_cls.entrypoint(
                        await cls.extract_request(request, handler_cls)
                    )

                    return JSONResponse(
                        status_code=response.status_code,
                        content=response.dict(),
                    )

                router.add_api_route(
                    handler_cls.url_prefix,
                    handler,
                    methods=[handler_cls.method],
                )

            app.include_router(
                router,
                prefix=f'{application.url_prefix}{router_item.url_prefix}'
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
    async def extract_request(cls, request: Request, handler: Handler) -> DataRequest:
        try:
            data = await request.json()
        except:
            data = {}

        return DataRequest(
            data=handler.request_data(**data),
        )

    @classmethod
    def error_handler(cls, request, exc):
        raise errors.NotFoundEngineError(
            args={
                'path': request.url.path,
            }
        )
