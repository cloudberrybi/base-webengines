import os

from pydantic import BaseModel


class WebAppSettings(BaseModel):
    host: str =  os.environ.get('WEB_HOST', '127.0.0.1')
    port: int =  int(os.environ.get('WEB_PORT', 8811))
    log_level: str = os.environ.get('WEB_LOG_LEVEL', 'info')
