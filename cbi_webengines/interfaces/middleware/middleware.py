from typing import Any

from ..data_request import DataRequest
from ..data_response import DataResponse


class Middleware:
    next: Any | None = None
    handler: Any | None = None

    def __init__(self, next: Any | None = None, handler: Any | None = None, **params):
        self.next = next
        self.handler = handler

        self.init_middleware(**params)

    def init_middleware(self, **params):
        pass

    async def process_request(self, request: DataRequest) -> DataRequest:
        return request
    
    async def process_response(self, response: DataResponse) -> DataResponse:
        return response

    async def do(self, request: DataRequest) -> DataResponse:
        request = await self.process_request(request)

        if self.next:
            response = await self.next.do(request)
        elif self.handler:
            response = await self.handler.do(request)

        response = await self.process_response(response)

        return response
