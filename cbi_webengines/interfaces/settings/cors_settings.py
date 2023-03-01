from typing import List

from pydantic import BaseModel


class CORSSettings(BaseModel):
    allow_origins: List[str] = ['*']
    allow_credentials: bool = True
    allow_methods: List[str] = ['*']
    allow_headers: List[str] = ['*']
