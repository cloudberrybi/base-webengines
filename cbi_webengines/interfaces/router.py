from typing import Any, List, Type, Tuple

from .handler import Handler
from .middleware import Middleware


class Router:
    _application: Any
    url_prefix: str
    handlers: List[Type[Handler]] = []
    middleware: List[Tuple[Middleware, dict]] = []

    def __init__(self, url_prefix: str):
        self.url_prefix = url_prefix

    @property
    def application(self):
        return self._application

    @application.setter
    def application(self, value):
        self._application = value

    def add_middleware(self, middleware: Type[Middleware], **params):
        middleware_item = (middleware, params)
        if middleware_item not in self.middleware:
            self.middleware.append(middleware_item)

    def connect_handler(self, handler: Type[Handler]):
        handler.router = self
        self.handlers.append(handler)
