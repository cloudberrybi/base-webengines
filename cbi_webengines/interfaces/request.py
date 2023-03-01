from typing import List

from pydantic import BaseModel

from .header import Header


class Request(BaseModel):
    headers: List[Header] = []

    def header(self, name: str) -> str | None:
        for hd in self.headers:
            if hd.name == name:
                return hd.value
            
        return None
