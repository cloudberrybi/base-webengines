from typing import List

from pydantic import BaseModel

from .header import Header


class DataRequest(BaseModel):
    data: BaseModel | None = None
    headers: List[Header] = []

    def get_header(self, name: str) -> str | None:
        for hd in self.headers:
            if hd.name == name:
                return hd.value
            
        return None
