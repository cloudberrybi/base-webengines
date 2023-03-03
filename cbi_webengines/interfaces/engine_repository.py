from typing import Any

from .data_request import DataRequest


class EngineRepository:
    @classmethod
    def create_engine_app(cls, application) -> Any: # ignore_coverage
        raise NotImplementedError()
    
    @classmethod
    async def extract_request(cls, request, handler) -> DataRequest: # ignore_coverage
        raise NotImplementedError()
