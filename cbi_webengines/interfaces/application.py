import asyncio

from typing import Type, Any, List, Tuple

from cbi_webengines.interfaces.servers import Server

from .engine_repository import EngineRepository
from .router import Router
from .middleware import Middleware


class Application:
    _engine_app: Any = None
    engine_repository: Type[EngineRepository]
    server: Type[Server]
    url_prefix: str
    middleware: List[Tuple[Middleware, dict]] = []
    routers: List[Router] = []

    def __init__(self, engine_repository: Type[EngineRepository], server: Type[Server], url_prefix: str):
        self.engine_repository = engine_repository

        self.server = server
        self.url_prefix = url_prefix

    def connect_router(self, router: Router):
        router.application = self
        self.routers.append(router)

    def add_middleware(self, middleware: Type[Middleware], **params):
        middleware_item = (middleware, params)
        if middleware_item not in self.middleware:
            self.middleware.append(middleware_item)

    async def async_serve(self):
        await self.server.async_serve(app=self.get_engine_app())

    def serve(self):
        asyncio.run(self.async_serve())

    def get_engine_app(self) -> Any:
        if not self._engine_app:
            self._engine_app = self.engine_repository.create_engine_app(self)

        return self._engine_app
