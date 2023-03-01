from typing import Any

from .handler import Handler


class Router:
    _application: Any
    url_prefix: str
    routes: dict = {}

    def __init__(self, url_prefix: str):
        self.url_prefix = url_prefix

    @property
    def application(self):
        return self._application

    @application.setter
    def application(self, value):
        self._application = value

    def handle(self, route: str, handler: Handler):
        pass
