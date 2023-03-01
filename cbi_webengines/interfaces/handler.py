from typing import Any


class Handler:
    _router: Any

    @property
    def router(self):
        return self._router
    
    @router.setter
    def router(self, value):
        self._router = value
