from typing import Any, Type

from pydantic import BaseModel

from .data_request import DataRequest
from .data_response import DataResponse


class Handler:
    _router: Any
    url_prefix: str
    method: str = 'POST'
    request_data: Type[BaseModel] | None = None

    @property
    def router(self):
        return self._router
    
    @router.setter
    def router(self, value):
        self._router = value

    @classmethod
    async def entrypoint(cls, request: DataRequest) -> DataResponse:
        handler = cls()

        middleware_stack = list(cls.router.application.middleware + cls.router.middleware)
        middleware_stack.reverse()

        last_middleware = None
        for i, middleware_tuple in enumerate(middleware_stack):
            middleware_cls, middleware_params = middleware_tuple

            if i == 0:
                middleware = middleware_cls(handler=handler, **middleware_params)
            else:
                middleware = middleware_cls(next=last_middleware, **middleware_params)

            last_middleware = middleware

        if last_middleware:
            return await last_middleware.do(request)
        
        return await handler.do(request)


    async def do(self, request: DataRequest) -> DataResponse:
        raise NotImplementedError()
