import asyncio

from typing import Type, Any

from cbi_webengines.interfaces.engines import Engine
from cbi_webengines.interfaces.servers import Server

from .router import Router


class Application:
    _engine_app: Any = None
    engine: Type[Engine]
    server: Type[Server]
    url_prefix: str

    def __init__(self, engine: Type[Engine], server: Type[Server], url_prefix: str):
        self.engine = engine
        self.server = server
        self.url_prefix = url_prefix

    def connect_router(self, router: Router):
        router.application = self

    async def async_serve(self):
        await self.server.async_serve(app=self.get_engine_app())

    def serve(self):
        asyncio.run(self.async_serve())

    def get_engine_app(self) -> Any:
        if not self._engine_app:
            self._engine_app = self.engine.create_engine_app()
        
        return self._engine_app
